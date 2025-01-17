from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import timedelta
from django.contrib.auth import get_user_model
from .models import RefreshToken

User = get_user_model()

class AuthTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="password123")
        self.client = APIClient()
        self.register_url = "/api/register/"
        self.login_url = "/api/login/"
        self.refresh_token_url = "/api/refresh/"
        self.logout_url = "/api/logout/"
        self.me_url = "/api/me/"

    def test_register_user(self):
        data = {
            "email": "newuser@example.com",
            "password": "newpassword123"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("email", response.data)
        self.assertEqual(response.data["email"], data["email"])

    def test_register_user_invalid_data(self):
        response = self.client.post(self.register_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user(self):
        data = {
            "email": "testuser@example.com",
            "password": "password123"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)

    def test_login_user_invalid_credentials(self):
        data = {
            "email": "testuser@example.com",
            "password": "wrongpassword"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_me_view_authenticated(self):
        login_data = {
            "email": "testuser@example.com",
            "password": "password123"
        }
        login_response = self.client.post(self.login_url, login_data)

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", login_response.data)

        access_token = login_response.data["access_token"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        
        response = self.client.get(self.me_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("email", response.data)
        self.assertEqual(response.data["email"], self.user.email)

    def test_me_view_unauthenticated(self):
        response = self.client.get(self.me_url)     
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_refresh_token_success(self):
        login_data = {
            "email": "testuser@example.com",
            "password": "password123"
        }
        login_response = self.client.post(self.login_url, login_data)
        refresh_token = login_response.data["refresh_token"]

        response = self.client.post(self.refresh_token_url, {"refresh_token": refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)

    def test_refresh_token_invalid(self):
        response = self.client.post(self.refresh_token_url, {"refresh_token": "invalidtoken"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Invalid refresh token format"})
    

    def test_refresh_token_expired(self):
        expired_token = RefreshToken.objects.create(user=self.user)
        expired_token.expires_at = expired_token.created_at - timedelta(seconds=1)
        expired_token.save()

        response = self.client.post(self.refresh_token_url, {"refresh_token": expired_token.token})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_logout_user(self):
        login_data = {
            "email": "testuser@example.com",
            "password": "password123"
        }
        login_response = self.client.post(self.login_url, login_data)
        refresh_token = login_response.data["refresh_token"]

        response = self.client.post(self.logout_url, {"refresh_token": refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("success", response.data)

        self.assertFalse(RefreshToken.objects.filter(token=refresh_token).exists())

    def test_logout_user_no_token(self):
        response = self.client.post(self.logout_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

