from rest_framework.test import APITestCase
from .models import CustomUser, Channel
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


# Create your tests here.
class UsersAPITestCase(APITestCase):
    def setUp(self):
        self.admin = CustomUser.objects.create_superuser(username='admintest', password='admintest')
        self.channel = Channel.objects.create(
            user_id=self.admin,
            channel_name="Канал админа",
            description="Я ВЛАДИМИР ИЛЬИЧ НЕПРЕВЗОЙДЁННЫЙ ГЕНИЙ"
        )
        self.user_url = reverse('user-view', kwargs={'user_id': self.admin.pk})
        self.channel_url = reverse('channel-view', kwargs={'channel_id': self.channel.pk})
        
        self.user_not_own = APIClient()
        self.user_not_own.force_authenticate(user=CustomUser.objects.filter(pk=8))
        
        self.user_own = APIClient()
        self.user_own.force_authenticate(user=self.admin)
        self.update_data = {
            'channel_name': 'Этот канал захватил Сталин',
            'description': 'Всех расстреляем',
        }
    
    
    def test_check_channel_without_auth(self):
        response = self.client.get(self.channel_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    def test_update_channel_without_auth(self):
        response = self.client.put(self.channel_url, data=self.update_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    
    def test_update_channel_with_auth_not_own_user(self):
        response = self.user_not_own.put(self.channel_url, data=self.update_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_channel_with_auth_own_user(self):
        response = self.user_own.patch(self.channel_url, data=self.update_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)