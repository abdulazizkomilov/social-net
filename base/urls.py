from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    path('', views.home, name='home'),
    path('follow/<str:pk>/', views.add_user_room, name='add_user_room'),
    path('unfollow/<str:pk>/', views.remove_user_room, name='remove_user_room'),
    path('like/<str:pk>/', views.like_room, name='like_room'),
    path('sign-up/', views.registerPage, name='sign_up'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('room/<str:pk>/', views.room, name='room'),
    path('profile/<str:pk>/', views.user_profile, name='user_profile'),
    path('update-user/', views.updateUser, name="update-user"),
    path('profile/follow/<str:pk>/', views.user_follow, name='user_follow'),
    path('profile/unfollow/<str:pk>/', views.user_unfollow, name='user_unfollow'),
    path('create-room/', views.createRoom, name='create_room'),
    path('update-room/<str:pk>/', views.update_room, name='update_room'),
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete_room'),
]
