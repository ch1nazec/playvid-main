from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    phone_number = PhoneNumberField(region='RU', blank=True)


class Channel(models.Model):
    user_id = models.OneToOneField(CustomUser, related_name='user', on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='Channels/AvatarChannel/%Y/%m/%d/', blank=True)
    channel_name = models.CharField(max_length=100, blank=False, unique=True)
    slug_name = models.SlugField(max_length=100, blank=False, unique=True)
    created_date = models.DateField(auto_now_add=True, editable=False)
    description = models.TextField(blank=True)
    preview = models.ImageField(upload_to='Channels/PreviewsChannel/%Y/%m/%d/', blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug_name:
            self.slug_name = slugify(self.channel_name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.channel_name