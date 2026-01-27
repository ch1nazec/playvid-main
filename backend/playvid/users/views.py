from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from users.models import CustomUser, Channel
from users.serializers import UserSerializer, ChannelSerializer

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.response import Response


# Create your views here.
class IsOwnerOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_staff:
            return True
        
        if isinstance(obj, CustomUser):
            return obj.id == request.user.id
        
        if isinstance(obj, Channel):
            return obj.user_id.id == request.user.id
        
        if hasattr(obj, 'user'):
            return obj.user.id == request.user.id
        if hasattr(obj, 'owner'):
            return obj.owner.id == request.user.id
        
        return False


class CreateUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UsersListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    

class UserView(generics.RetrieveUpdateDestroyAPIView):
    """
    This API can be change data or check data users separately.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = 'user_id'
    
    
    def get_permissions(self):
        """
        Check on the users can all,
        since change data should only owner.
        """
        self.permission_classes = [AllowAny]
        
        if self.request.method in {'POST', 'PUT', 'DELETE', 'PATCH'}:
            self.permission_classes = [IsAuthenticated, IsOwnerOrStaff]
        return super().get_permissions()
    
    def get_queryset(self):
        import time
        time.sleep(3)

        return super().get_queryset()
    
    @method_decorator(cache_page(60 * 15, key_prefix='user-detail'))
    def get(self, request, *args, **kwargs):
        """
        If server not found user then give error or
        give data about user.
        """
        user_id = kwargs.get('user_id')
        instance = get_object_or_404(CustomUser, pk=user_id)
        serializer_data = UserSerializer(instance)
        
        return Response(serializer_data.data)


class ChannelListView(generics.ListAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = [AllowAny]

    @method_decorator(cache_page(60 * 15, key_prefix='channel-list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ChannelView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    lookup_url_kwarg = 'channel_id'
    
    
    # @method_decorator(cache_page(60 * 15, key_prefix='channel-detail'))
    # def get(self, request, *args, **kwargs):
    #     return super().get(request, *args, **kwargs)

    def get_permissions(self):
        """
        Check on the users can all,
        since change data should only owner.
        """
        self.permission_classes = [AllowAny]
        
        if self.request.method in {'POST', 'PUT', 'DELETE', 'PATCH'}:
            self.permission_classes = [IsAuthenticated, IsOwnerOrStaff]
        return super().get_permissions()