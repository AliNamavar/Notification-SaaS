from celery import shared_task
from django.utils import timezone
from .models import Notification
from utils.send_mail import send_email

@shared_task(bind=True, max_retries=3)
def send_notification_task(self, notification_id):
    notif = Notification.objects.get(id=notification_id)
    try:
        if notif.type == "email":
            send_email(
                subject=notif.subject,
                to=notif.to,
                context={"body": notif.body},
                template_name="emails/base.html",
            )
            notif.status = "sent"
            notif.provider_response = {"ok": True}
        elif notif.type == "sms":
            print(f"SMS to {notif.to}: {notif.body}")
            notif.status = "sent"
            notif.provider_response = {"ok": True}
        notif.processed_at = timezone.now()
        notif.save()
    except Exception as e:
        notif.status = "failed"
        notif.provider_response = {"error": str(e)}
        notif.attempts += 1
        notif.save()
        raise self.retry(exc=e, countdown=60)
