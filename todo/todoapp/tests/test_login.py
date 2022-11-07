import json
from django.test import TestCase
from django.test import Client
from django.urls import reverse

from todoapp.tests.factories import UserFactory


class TestRegistrationApi(TestCase):

    login_endpoint = reverse('login-api')
    user_email = "test-email@abc.com"
    user_password = "abcdef"

    def setUp(self) -> None:
        UserFactory.create(email=self.user_email, password=self.user_password)

    def test_register_user(self):
        payload = {"email": self.user_email, "password": self.user_password}

        client = Client()
        response = client.post(self.login_endpoint,
                               json.dumps(payload),
                               content_type="application/json")

        response_data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue("token" in response_data)
