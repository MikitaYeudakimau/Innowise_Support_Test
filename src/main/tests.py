from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import *


class TestMixin(APITestCase):
    """
    Default methods and attributes
    """
    create_user_url = "/auth/users/"
    get_token_url = reverse("jwt-create")
    ticket_list_url = reverse("ticket-list")
    data = {
        "email": "test@test.by",
        "username": "testuser",
        "password": "Asdfqwe123"
    }

    def create_account(self):
        """
        Create new account
        """
        response = self.client.post(self.create_user_url, self.data)
        return response

    def get_token(self):
        """
        Get JWT token:
        """
        response = self.client.post(self.get_token_url, self.data)
        self.token = response.data['access']

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)


class AccountTest(TestMixin):
    def test_create_account(self):
        """
        Ensure create new account
        """
        self.assertEqual(self.create_account().status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get(username="testuser").username, "testuser")


class JWTAuthenticationTest(TestMixin):
    def test_get_ticket_list_authenticated(self):
        self.create_account()
        self.get_token()
        self.authenticate()
        response = self.client.get(self.ticket_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_ticket_list_non_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.ticket_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
