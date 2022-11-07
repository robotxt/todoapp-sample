import json
from django.test import TestCase
from django.test import Client
from django.urls import reverse


class TestRegistrationApi(TestCase):

    registration_endpoint = reverse('registration-api')

    def test_register_user(self):
        payload = {
            "email": "test-email@abc.com",
            "password": "abcdef",
            "firstname": "bilbo",
            "lastname": "bagins"
        }

        client = Client()
        response = client.post(self.registration_endpoint,
                               json.dumps(payload),
                               content_type="application/json")

        response_data = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertTrue("token" in response_data)
