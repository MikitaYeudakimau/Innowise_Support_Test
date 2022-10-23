from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Status, User


class TestMixin(APITestCase):
    """
    Default methods and attributes
    """
    create_user_url = "/auth/users/"
    get_token_url = reverse("jwt-create")
    ticket_list_url = reverse("ticket-list")
    status_list_url = reverse("status-list")
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

    def create_admin_account(self):
        """
        Create account with admin rules
        """
        response = self.client.post(self.create_user_url, self.data)
        admin = User.objects.get(username="testuser")
        admin.is_staff = True
        admin.save()
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
    """
    Tests for creation new accounts
    """

    def test_create_account(self):
        """
        Ensure create new account
        """
        self.assertEqual(self.create_account().status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get(username="testuser").username, "testuser")

    def test_create_admin_account(self):
        """
        Ensure create account with admin rules
        """
        self.assertEqual(self.create_admin_account().status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get(username="testuser").is_staff, True)


class JWTAuthenticationTest(TestMixin):
    """
    Test for normal operation for JWTAuthentication accessing ticket-list page
    """

    def test_get_ticket_list_authenticated(self):
        """
        Test getting ticket list witt JWT authentication
        """
        self.create_account()
        self.get_token()
        self.authenticate()
        response = self.client.get(self.ticket_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_ticket_list_non_authenticated(self):
        """
        Test forbidding request for non-authenticated users
        """
        self.client.force_authenticate(user=None)
        response = self.client.get(self.ticket_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class StatusTest(TestMixin):
    """
    Test status page for prohibiting access not-admin user adding new statuses
    """
    status_data = {"status": "status"}

    def test_prohibit_access(self):
        """
        Test prohibiting access for non-admin user
        """
        self.create_account()
        self.client.login(username="testuser", password="Asdfqwe123")
        response = self.client.get(self.status_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_status(self):
        """
        Test addition status using session_authenticate
        """
        self.create_admin_account()
        self.client.login(username="testuser", password="Asdfqwe123")
        response = self.client.post(self.status_list_url, self.status_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Status.objects.get(status="status").status, "status")
