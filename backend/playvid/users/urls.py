from django.urls import include, path
from users import views


urlpatterns = [
    path('', views.UsersListView.as_view(), name='users-list-view'),
    path('create/', views.CreateUserView.as_view(), name='create-user-view'),
    path('<int:user_id>/', views.UserView.as_view(), name='user-view'),
    path('channel/', views.ChannelListView.as_view(), name='channel-list-view'),
    path('channel/<int:channel_id>/', views.ChannelView.as_view(), name='channel-view'),
]

