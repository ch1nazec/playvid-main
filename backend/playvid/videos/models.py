from django.db import models
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.core.validators import FileExtensionValidator
from users.models import Channel, CustomUser
from mptt.models import MPTTModel, TreeForeignKey

import uuid


# Create your models here.
class Tag(models.Model):
    name_tag = models.CharField(unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    
    def __str__(self):
        return f'{self.name_tag} - {self.slug}'
        

@receiver(pre_save, sender=Tag)
def generate_tag_slug(sender, instance, **kwargs):
    # Если slug уже есть — ничего не делаем
    if instance.slug:
        return
    
    # Генерируем slug из name_tag
    if instance.name_tag and instance.name_tag.strip():
        base_slug = slugify(instance.name_tag)
    else:
        base_slug = f'tag-{uuid.uuid4().hex[:8]}'
    
    # Убедимся, что base_slug не пустой
    if not base_slug:
        base_slug = f'tag-{uuid.uuid4().hex[:8]}'
    
    # Проверяем уникальность slug (игнорируем текущий instance, если он уже сохранён)
    instance.slug = base_slug
    counter = 1
    while Tag.objects.filter(slug=instance.slug).exclude(pk=instance.pk).exists():
        instance.slug = f'{base_slug}-{counter}'
        counter += 1


class Videos(models.Model):
    channel_id = models.ForeignKey(Channel, verbose_name='Канал', related_name='channel', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=False, verbose_name='Название видео',)
    description = models.TextField(max_length=3000, blank=True, verbose_name='Описание',)
    preview = models.ImageField(upload_to='Channels/PreviewVideo/', blank=True)
    video = models.FileField(upload_to='Channels/Video/%Y/%m/%d/', max_length=1000, validators=[FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mov', 'mkv'])])
    date_upload = models.DateTimeField(auto_now_add=True)
    public_video = models.BooleanField(default=True)
    tag = models.ManyToManyField(Tag, through='VideoTag', related_name='videos', blank=True)
    
    def __str__(self):
        return self.name


class ViewVideo(models.Model):
    video = models.ForeignKey(Videos, on_delete=models.CASCADE, related_name='view_video')
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        models.Index(fields=['video', 'user']),
        models.Index(fields=['video', 'ip_address']),


class VideoLike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video = models.ForeignKey(Videos, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'video']


class VideoRepost(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video = models.ForeignKey(Videos, on_delete=models.CASCADE)


class VideoTag(models.Model):
    video = models.ForeignKey(Videos, on_delete=models.CASCADE,)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['video', 'tag']


class Comment(MPTTModel):
    author = models.ForeignKey(CustomUser, related_name='author', on_delete=models.CASCADE)
    video = models.ForeignKey(Videos, related_name='comments', on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True,)
    
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_hidden = models.BooleanField(default=False)
    
    class MPTTMeta:
        order_insertion_by = ['created_at']
        
    class Meta:
        indexes = [
            models.Index(fields=['video', 'created_at',]),
            models.Index(fields=['video', 'parent',]),
        ]
        ordering = ['-created_at']
    
    @property
    def reply_count(self):
        return self.children.count()
    
    def __str__(self):
        return f"{self.author.username}'s comment"