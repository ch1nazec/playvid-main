from django.utils import timezone
from datetime import timedelta
from .models import ViewVideo
from django.contrib.auth.models import AnonymousUser
from rest_framework import filters


class ViewCounter:
    @staticmethod
    def add_view(video, request):
        user = request.user if request.user else None
        ip_address = request.META.get('REMOTE_ADDR')
        has_viewed = False
        
        if user and not isinstance(user, AnonymousUser):
            data, created = ViewVideo.objects.get_or_create(
                user=user,
                video=video,
                defaults={'ip_address': None})
        else:
            data, created = ViewVideo.objects.get_or_create(
                ip_address=ip_address,
                video=video,
                defaults={'user': None})
        
        return True if created else None


