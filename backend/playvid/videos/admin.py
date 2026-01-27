from django.contrib import admin
from django import forms
from django.utils.text import slugify
from mptt.admin import DraggableMPTTAdmin
from .models import (
    Tag, Videos, VideoLike, VideoRepost, VideoTag, Comment, Channel
)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['name_tag']
    list_display = ['name_tag']
    ordering = ['name_tag']


# class VideoTagInline(admin.TabularInline):
#     model = VideoTag
#     extra = 1
#     autocomplete_fields = ['tag']


class VideoAdminForm(forms.ModelForm):
    """Форма с полем для ввода тегов через запятую"""
    tags_input = forms.CharField(
        label='Теги',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'cols': 80,
            'placeholder': 'Теги через , без пробелов'
        }),
        help_text='Введите теги через запятую. Существующие теги будут связаны, новые созданы автоматически.'
    )
    
    class Meta:
        model = Videos
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Заполняем поле существующими тегами
            video_tags = VideoTag.objects.filter(video=self.instance)
            tag_names = [vt.tag.name_tag for vt in video_tags]
            self.initial['tags_input'] = ', '.join(tag_names)


@admin.register(Videos)
class VideosAdmin(admin.ModelAdmin):
    form = VideoAdminForm
    list_display = ['name', 'channel_id', 'date_upload', 'tags_display', 'public_video']
    
    list_display = ['name', 'channel_id', 'date_upload', 'public_video', 'likes_count', 'reposts_count', 'comments_count']
    list_filter = ['public_video', 'date_upload', 'channel_id']
    search_fields = ['name', 'description', 'channel_id__name']
    date_hierarchy = 'date_upload'
    readonly_fields = ['date_upload']
    autocomplete_fields = ['channel_id']

    def likes_count(self, obj):
        return obj.videolike_set.count()
    likes_count.short_description = 'Лайки'

    def reposts_count(self, obj):
        return obj.videorepost_set.count()
    reposts_count.short_description = 'Репосты'

    def comments_count(self, obj):
        return obj.comments.count()
    comments_count.short_description = 'Комментарии'
    
    def tags_display(self, obj):
        tags = VideoTag.objects.filter(video=obj).select_related('tag')[:5]
        if not tags:
            return "-"
        tag_names = [t.tag.name_tag for t in tags]
        result = ", ".join(tag_names)
        total = VideoTag.objects.filter(video=obj).count()
        if total > 5:
            result += f" (+{total - 5})"
        return result
    tags_display.short_description = 'Теги'
    
    # Переопределяем сохранение для обработки тегов
    def save_model(self, request, obj, form, change):
        # Сохраняем видео
        super().save_model(request, obj, form, change)
        
        # Обрабатываем теги
        tags_input = form.cleaned_data.get('tags_input', '')
        
        if tags_input:
            # Удаляем старые связи (опционально)
            try:
                VideoTag.objects.filter(video=obj).delete()
            
                # Обрабатываем каждый тег
                tag_names = [t.strip() for t in tags_input.split(',') if t.strip()]
                
                for tag_name in tag_names:
                    # Создаем или получаем тег
                    tag, created = Tag.objects.get_or_create(name_tag=tag_name)
                    # Создаем связь с видео
                    VideoTag.objects.get_or_create(video=obj, tag=tag)
            except BaseException as err:
                print(err)


@admin.register(VideoLike)
class VideoLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'video']
    search_fields = ['user__username', 'video__name']
    autocomplete_fields = ['user', 'video']


@admin.register(VideoRepost)
class VideoRepostAdmin(admin.ModelAdmin):
    list_display = ['user', 'video']
    search_fields = ['user__username', 'video__name']
    autocomplete_fields = ['user', 'video']


@admin.register(Comment)
class CommentAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'video', 'author', 'created_at', 'is_hidden')
    list_display_links = ('indented_title',)
    list_filter = ['is_hidden', 'created_at', 'video']
    search_fields = ['text', 'author__username', 'video__name']
    autocomplete_fields = ['author', 'video']

    # Чтобы коротко показывало текст комментария в списке
    def indented_title(self, instance):
        return f"{instance.text[:50]}..."
    indented_title.short_description = 'Комментарий'