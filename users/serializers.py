from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import RefreshToken
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from constance import config

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = User.objects.filter(email=email).first()

        if user and user.check_password(password):
            return user
        raise serializers.ValidationError("Invalid email or password")

class TokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.UUIDField(read_only=True)

    def create_tokens(self, user):
        access_token_payload = {
            "user_id": user.id,
            "exp": datetime.utcnow() + timedelta(seconds=config.ACCESS_TOKEN_LIFETIME),
            "iat": datetime.utcnow(),
        }
        access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm="HS256")
        refresh_token = RefreshToken.objects.create(user=user)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token.token,
        }
    

