from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login', views.loginuser ,name='loginuser'),
    path('logout', views.logoutuser, name='logoutuser'),
    path('', views.index, name='index'),
    path('profile_list/', views.profile_list, name = "profile_list"),
    path('profile/<int:pk>', views.profile, name= "profile"),
    path('followers/<int:pk>', views.followers, name= "followers"),
    path('register', views.register, name="register"),
    path('update_user', views.update_user, name="update_user"),
    path('tweet_like/<int:pk>', views.tweet_likes, name = "tweet_likes"),
    path('tweet_show/<int:pk>', views.tweet_show, name = "tweet_show"),
    path('unfollow/<int:pk>', views.unfollow, name = "unfollow"),
    path('follow/<int:pk>', views.follow, name = "follow")
]