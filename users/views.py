from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from notifications.models import APIKey
from .models import User
from .serializer import LoginSerializer, SignUpSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class SignUp(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create(
                phone=serializer.validated_data['phone'],
                user_name=serializer.validated_data['user_name'],
            )
            user.set_password(serializer.validated_data['password'])
            user.save()

            raw, prefix, hashed = APIKey.generate_key()

            api_key = APIKey.objects.create(
                user=user,
                hashed_key=hashed,
                prefix=prefix,
                name=user.user_name
            )
            return JsonResponse({
                "message": "ثبت‌نام موفق",
                "user": {
                    "id": user.id,
                    "phone": user.phone,
                    "user_name": user.username,
                },
                "api_key": raw
            }, status=status.HTTP_201_CREATED)
        return JsonResponse({
            'erros': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = User.objects.filter(phone=serializer.validated_data['phone']).first()
            token = RefreshToken.for_user(user)

            return JsonResponse({
                'access': str(token.access_token),
                'refresh': str(token),
                'user': {
                    'id': user.id,
                    'phone': user.phone,
                    'user_name': user.user_name,
                }
            })
        return JsonResponse({
            'error': serializer.errors
        })
