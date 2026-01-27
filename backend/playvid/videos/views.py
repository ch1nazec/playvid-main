from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from .models import Videos, Comment, VideoLike, VideoRepost, Tag, ViewVideo
from users.models import Channel
from .serializers import VideoSerializer, CommentSerializer, TagSerializer
from rest_framework import viewsets, serializers, status, views, filters
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly, BasePermission
from django_filters.rest_framework import DjangoFilterBackend
from django.http import FileResponse, StreamingHttpResponse
from wsgiref.util import FileWrapper
import os

from .services import ViewCounter


class IsOwnerOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not bool(request.user and request.user.is_authenticated):
            return False
        
        if request.user.is_staff:
            return True
        
        if isinstance(obj, Videos):
            return obj.channel_id.user_id == request.user.id
        return False


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def toggle_like(request, video_id):
    user = request.user
    video = Videos.objects.get(pk=video_id)

    with transaction.atomic():
        like, created_at = VideoLike.objects.get_or_create(
            user=user,
            video=video,
        )

        if not created_at:
            like.delete()
            return Response(data={'status': 'unlike'}, status=status.HTTP_204_NO_CONTENT)
        return Response(data={'status': 'like'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def toggle_repost(request, video_id):
    user = request.user
    video = Videos.objects.get(pk=video_id)

    repost, created_at = VideoRepost.objects.get_or_create(video=video, user=user)
    return Response(data={'status': 'repost'})


# Create your views here.
class VideosListAPIView(generics.ListAPIView):
    queryset = Videos.objects.select_related('channel_id').all()
    serializer_class = VideoSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    options = ['exact', 'icontains']
    filterset_fields = {
        'name': options,
        'tag__name_tag': options,
        'description': options,
    }
    search_fields = ['name']
    ordering_fields = ['id', 'date_upload']
    
    


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        video_id = self.request.query_params.get('video_id')
        queryset = Comment.objects.all()
        
        if video_id:
            queryset = queryset.objects.filter(
                video_id=video_id,
                parent__isnull=True,
                is_hidden=False,
            )
        return queryset
    
    def perform_create(self, serializer):
        video = self.request.POST.get('video')
        if not video:
            raise serializers.ValidationError(
                {'video_id': 'Это поле обязательно'}
            )
        
        video = get_object_or_404(Videos, id=video)
        serializer.save(
            video=video,
            author=self.request.user
        )


class VideoUploadAPI(views.APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, *args, **kwargs):
        serializer = VideoSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(channel_id=request.user.user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Videos.objects.all()
    serializer_class = VideoSerializer
    lookup_url_kwarg = "video_id"

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if not self.request.method == 'GET':
            self.permission_classes = [IsOwnerOrStaff]

        return super().get_permissions()
    
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        video = self.get_object()
        ViewCounter.add_view(video, request)
        
        return response


class TagDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_url_kwarg = 'tag_name'
    
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if not self.request.method == 'GET':
            self.permission_classes = [IsOwnerOrStaff]

        return super().get_permissions()
    
