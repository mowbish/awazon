from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class UserTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123',
            phone_number='1234567890'
        )

    def test_create_user(self):
        url = reverse('user-list')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'phone_number': '0987654321'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(username='newuser').email, 'newuser@example.com')

    def test_get_user_profile(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('user-profile')
        self.client.force_authenticate(user=self.user)  # Ensure authentication
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_update_user_profile(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('user-profile')
        self.client.force_authenticate(user=self.user)  # Ensure authentication
        data = {'email': 'updatedemail@example.com'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(username='testuser').email, 'updatedemail@example.com')

    def test_token_obtain(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_refresh(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        refresh_token = response.data['refresh']

        url = reverse('token_refresh')
        data = {
            'refresh': refresh_token
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
