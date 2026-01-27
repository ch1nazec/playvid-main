from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from users.models import CustomUser
from django.core.cache import cache


@receiver([post_save, post_delete], sender=CustomUser)
def invalidated_user_cache(sender, instance, **kwargs):
    cache.delete_many([
        '*user-detail*',
        'channel-detail',
        'channel-list',
    ])