import uuid
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import RefreshToken
from .authentication import CustomJWTAuthentication
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, TokenSerializer
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={201: UserSerializer, 400: openapi.Response('Bad Request', RegisterSerializer)},
        operation_summary="Register a new user"
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = {
                'id': user.id,
                'email': user.email,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={200: TokenSerializer, 400: openapi.Response('Bad Request', LoginSerializer)},
        operation_summary="Log in a user"
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token_serializer = TokenSerializer()
            tokens = token_serializer.create_tokens(user)
            return Response(tokens, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=TokenSerializer,
        responses={200: TokenSerializer, 400: openapi.Response('Bad Request', TokenSerializer)},
        operation_summary="Refresh access token using refresh token"
    )
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            uuid.UUID(refresh_token) 
        except ValueError:
            return Response({"error": "Invalid refresh token format"}, status=status.HTTP_400_BAD_REQUEST)

        token_obj = RefreshToken.objects.filter(token=refresh_token).first()
        if token_obj and not token_obj.is_expired():
            token_obj.delete()
            token_serializer = TokenSerializer()
            tokens = token_serializer.create_tokens(token_obj.user)
            return Response(tokens, status=status.HTTP_200_OK)

        return Response({"error": "Invalid or expired refresh token"}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
  
    @swagger_auto_schema(
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={'refresh_token': openapi.Schema(type=openapi.TYPE_STRING)}),
        responses={200: openapi.Response('Successful logout'), 400: openapi.Response('Bad Request')},
        operation_summary="Log out a user"
    )
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            RefreshToken.objects.filter(token=refresh_token).delete()
            return Response({"success": "User logged out."}, status=status.HTTP_200_OK)
        return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

class MeView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]  

    @swagger_auto_schema(
        responses={200: UserSerializer},
        operation_summary="Get current user information"
    )
    def get(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={200: UserSerializer, 400: openapi.Response('Bad Request')},
        operation_summary="Update current user information"
    )
    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)