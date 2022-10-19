from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import *


class TestMixin():


class AccountTest(APITestCase):
    def test_create_account(self):
        """
        Ensure we create new account

        """
        url = "/auth/users/"
        data = {
            "email": "test@test.by",
            "username": "testuser",
            "password": "Asdfqwe123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get(username="testuser").username, "testuser")


class TicketJWTAuthenticationTest(APITestCase):
    create_user_url = "/auth/users/"
    get_token_url = reverse("jwt-create")
    ticket_list_url = reverse("ticket-list")
    data = {
        "username": "testuser",
        "password": "Asdfqwe123"
    }

    def get_token(self):
        self.user = self.client.post(self.create_user_url, self.data)
        response = self.client.post(self.get_token_url, self.data)
        self.token = response.data['access']
        self.authenticate()

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    def test_get_ticket_list_authenticated(self):
        self.get_token()
        self.authenticate()
        response = self.client.get(self.ticket_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_ticket_list_non_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.ticket_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


