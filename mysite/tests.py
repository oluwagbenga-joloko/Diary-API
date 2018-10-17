from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class RootTest(APITestCase):
    
    def test_root(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('entries', response.data)
        self.assertIn('users', response.data)
