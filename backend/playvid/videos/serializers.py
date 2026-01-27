from rest_framework import serializers
from .models import Videos, Tag, Comment
from pprint import pprint


def validate_data(value):
    if value < 0:
        return serializers.ValidationError('Like must be only greate or equal 0')
    return value


class TagSerializer(serializers.ModelSerializer):
    list_field = serializers.CharField(max_length=5000,
        write_only=True, 
        required=False,
        allow_blank=True)
    class Meta:
        model = Tag
        fields = ['name_tag', 'list_field']
    
    def create(self, validated_data):
        list_field = validated_data['list_field']
        if list_field:
            tags = [tag.strip() for tag in list_field.split(',')]
            
            data = []
            for tag in tags:
                tag_obj, _ = Tag.objects.get_or_create(name_tag=tag)
                data.append(tag_obj)
                
        return data
    
    def update(self, instance, validated_data):
        list_field = validated_data['list_field']
        if list_field:
            tags = [tag.strip() for tag in list_field.split(',')]
            
            data = []
            for tag in tags:
                tag_obj, _ = Tag.objects.get_or_create(name_tag=tag)
                data.append(tag_obj)
                
        return super().update(instance, validated_data)


class VideoSerializer(serializers.ModelSerializer):
    """
    This serializers return lists all video from db
    """

    tag_field = serializers.CharField(write_only=True, required=False, allow_blank=True)
    tags = TagSerializer(many=True, read_only=True)
    channel_id = serializers.PrimaryKeyRelatedField(read_only=True)

    channel_name = serializers.CharField(source='channel_id.channel_name', read_only=True)
    channel_avatar = serializers.SerializerMethodField()
    channel_slug = serializers.CharField(source='channel_id.slug_name', read_only=True)

    class Meta:
        model = Videos
        fields = (
            'id',
            'name', 'description',
            'preview', 'video', 
            'date_upload', 'public_video',
            'tag_field', 'tags', 'channel_id',
            'channel_name', 'channel_avatar', 'channel_slug'
        )
        read_only_fields = ['date_upload']
    
    def get_channel_avatar(self, obj):
        if obj.channel_id and obj.channel_id.avatar:
            return obj.channel_id.avatar.url
        return

    def validate_like_score(self, value: int):
        return validate_data(value)
    
    def validate_dislike_score(self, value: int):
        return validate_data(value)
    
    def validate_repost_score(self, value: int):
        return validate_data(value)
    
    def validate_tag_list(self, value: str):
        if len(value) > 10_000:
            return serializers.ValidationError
        
    def create(self, validated_data):
        tag_input = validated_data.pop('tag_fields', '')
        video = Videos.objects.create(**validated_data)

        if tag_input:
            tag_list = [tag for tag in tag_input.split(',') if tag.strip()]
            for tag_name in tag_list:
                tag = Tag.objects.get_or_create(
                    name_tag=tag_name,
                )
                video.tag.add(tag)
        return video
    
    def update(self, instance, validated_data):
        tags_str = validated_data.pop('tag_field', '')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if tags_str is not None:
            instance.tag.clear()

            tag_list = [tag for tag in tags_str.split(',') if tag.strip()]
            for tag in tag_list:
                tag, _ = Tag.objects.get_or_create(
                    name_tag=tag,
                )
                instance.tag.add(tag)
        
        return instance


class RecursiveCommentSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        serializers = CommentSerializer(value, context=self.context)
        return serializers.data


class CommentSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'author', 'video', 'parent', 'children',
            'text', 'created_at', 'is_hidden',
        ]
    
    def get_children(self, obj):
        return CommentSerializer(obj.children.all(), many=True).data 
    
    def validate(self, attrs):
        video = attrs.get('video')
        parent_video = attrs.get('parent').get('video')
        
        print(video, parent_video)
        return super().validate(attrs)