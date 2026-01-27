from django.urls import path, include
from .views import VideosListAPIView, CommentViewSet, VideoDetailAPI, toggle_like, toggle_repost, VideoUploadAPI
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'comment', CommentViewSet, basename='comment')

urlpatterns = [
    path('', VideosListAPIView.as_view(), name='video-list'),
    path('<int:video_id>/', VideoDetailAPI.as_view(), name='video-detail'),
    path('<int:video_id>/like/', toggle_like, name='video-like'),
    path('<int:video_id>/repost/', toggle_repost, name='video-repost'),
    path('upload/', VideoUploadAPI.as_view(), name='video-upload'),
]

urlpatterns += router.urls