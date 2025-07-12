from django.urls import path
from . import views


app_name = 'userProfile'

urlpatterns = [
    path('<str:username>/', views.profile_view, name='profile_view'),
    path('<str:username>/edit/', views.edit_profile, name='edit_profile'),
    # path('<str:username>/followers/', views.follower_list, name='follower_list'),
    # path('<str:username>/following/', views.following_list, name='following_list'),
    # path('<str:username>/follow/', views.follow_user, name='follow_user'),
    # path('<str:username>/unfollow/', views.unfollow_user, name='unfollow_user'),
]
