from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import *

class AccountTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we create new account

        """
        url = "/api/auth/users/"
        data = {
            "email" : "test@test.by",
            "username" : "testuser",
            "password" : "Asdfqwe123"
        }
        response = self.client.post(url,data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get(username="testuser").username,"testuser")
