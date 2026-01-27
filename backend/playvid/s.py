import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'playvid.settings')
django.setup()
from django.utils.text import slugify
from users.models import CustomUser, Channel
from videos.models import Videos, Tag


Videos.objects.all().delete()