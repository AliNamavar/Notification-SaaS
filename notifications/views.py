from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.timezone import now
from rest_framework import status
# Create your views here.
from rest_framework import authentication, exceptions
import hashlib

from rest_framework.views import APIView

from notifications.models import APIKey, Notification
from notifications.serializer import NotificationSerializer


class APIKeyAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        raw = request.headers.get('X-Api-Key') or request.query_params.get('api_key')
        if not raw:
            return None
        prefix = raw.split('-', 1)[0]
        hashed = hashlib.sha256(raw.encode()).hexdigest()
        try:
            key = APIKey.objects.get(prefix=prefix, hashed_key=hashed, revoked=False)
        except APIKey.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid API Key')
        key.last_used = timezone.now()
        key.save(update_fields=['last_used'])
        return (key.user, key)


from .task import send_notification_task


class SentNotifications(APIView):
    authentication_classes = [APIKeyAuthentication]
    permission_classes = []

    def post(self, request):
        profile = getattr(request.user, "userprofile", None)
        if not profile or not profile.plan:
            return JsonResponse({"error": "User has no plan assigned"}, status=403)

        plan = profile.plan

        start_of_month = now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        count_this_month = Notification.objects.filter(
            user=request.user,
            created_at__gte=start_of_month
        ).count()

        if count_this_month >= plan.monthly_quota:
            return JsonResponse(
                {"error": "Quota exceeded, please upgrade your plan"},
                status=429
            )

        data = request.data

        recipients = data.get("to")
        if isinstance(recipients, list):
            notifications = []
            for r in recipients:
                single_data = data.copy()
                single_data["to"] = r

                serializer = NotificationSerializer(data=single_data)
                if serializer.is_valid():
                    serializer.save(user=request.user, api_key=request.auth)
                    notif = serializer.instance
                    from .task import send_notification_task
                    send_notification_task.delay(str(notif.id))
                    notifications.append({"id": notif.id, "to": notif.to, "status": notif.status})
                else:
                    return JsonResponse({"errors": serializer.errors}, status=400)

            return JsonResponse({"count": len(notifications), "notifications": notifications}, status=201)

        serializer = NotificationSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user, api_key=request.auth)
            notif = serializer.instance
            from .task import send_notification_task
            send_notification_task.delay(str(notif.id))
            return JsonResponse({"request_id": notif.id, "status": notif.status}, status=201)

        return JsonResponse({"errors": serializer.errors}, status=400)


class Notification_filter(APIView):
    authentication_classes = [APIKeyAuthentication]
    permission_classes = []

    def get(self, request, request_id=None):
        queryset = Notification.objects.filter(user=request.user)


        type = request.GET.get('type')
        status = request.GET.get('status')

        if type:
            queryset = queryset.filter(type=type)
        if status:
            queryset = queryset.filter(status=status)

        if request_id:
            notifications: Notification = Notification.objects.filter(id=request_id).first()
            if not notifications:
                return JsonResponse({"error": "Notification not found"}, status=404)

            return JsonResponse({
                "id": notifications.id,
                "type": notifications.type,
                "to": notifications.to,
                "status": notifications.status,
                "created_at": notifications.created_at,
                "processed_at": notifications.processed_at
            })

        notifications = queryset.all()

        data = [{
            "id": n.id,
            "type": n.type,
            "to": n.to,
            "status": n.status,
            "created_at": n.created_at,
            "processed_at": n.processed_at
        } for n in notifications]
        return JsonResponse({"notifications": data}, safe=False)
