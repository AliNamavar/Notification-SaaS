from rest_framework import serializers

from users.models import User


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()


    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')

        user : User = User.objects.filter(phone=phone).first()

        if not user or not user.check_password(password):
            return serializers.ValidationError('نام کاربری یا پسوورد اشتباه است')

        return attrs


class SignUpSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    user_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    password_r = serializers.CharField(required=True)

    def validate(self, attrs):
        phone = attrs.get('phone')
        user_name = attrs.get('user_name')
        password = attrs.get('password')
        password_r = attrs.get('password_r')

        if password != password_r:
            raise serializers.ValidationError('پسوورد و تکرار آن با هم برار نبستند.')

        user = User.objects.filter(phone=phone).first()
        if user:
            raise serializers.ValidationError('این شماره ی موبایل قبلا استفاده شده است.')

        return attrs

