from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from users.models import CustomUser, Channel
from .models import Videos, ViewVideo
from django.core.files.uploadedfile import SimpleUploadedFile


# Create your tests here.
class VideoViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = CustomUser.objects.create_user(
            username='test',
            password='test'
        )

        self.channel = Channel.objects.create(
            user_id=self.user,
            channel_name='test channel'
        )

        video_file = SimpleUploadedFile(
            "test.mp4",
            b"fake video content",
            content_type="video/mp4"
        )

        self.video = Videos.objects.create(
            channel_id=self.channel,
            name='test video',
            video=video_file,
            public_video=True
        )

        self.client.force_authenticate(user=self.user)
    
    def test_with_different_api(self):
        url = f'/api/video/{self.video.pk}/'
        
        different_ips = [
            '192.168.1.1',
            '10.0.0.1', 
            '172.16.0.1',
            '127.0.0.1',
            '8.8.8.8'
        ]
        
        for ip in different_ips:
            response = self.client.get(
                url,
                REMOTE_ADDR=ip,
                HTTP_USER_AGENT='Test browser',
            )
        print(ViewVideo.objects.filter(video=self.video).count())