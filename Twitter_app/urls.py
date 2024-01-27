from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('', views.loginuser ,name='loginuser'),
    path('logout', views.logoutuser, name='logoutuser'),
    path('profile_list/', views.profile_list, name = "profile_list"),
    path('profile/<int:pk>', views.profile, name= "profile"),
    path('profile/followers/<int:pk>', views.followers, name= "followers"),
    path('profile/follows/<int:pk>', views.follows, name= "follows"),
    path('register', views.register, name="register"),
    path('update_user', views.update_user, name="update_user"),
    path('tweet_like/<int:pk>', views.tweet_likes, name = "tweet_likes"),
    path('tweet_show/<int:pk>', views.tweet_show, name = "tweet_show"),
    path('unfollow/<int:pk>', views.unfollow, name = "unfollow"),
    path('follow/<int:pk>', views.follow, name = "follow"),
    path('delete_tweet/<int:pk>', views.delete_tweet, name = "delete_tweet"),
    path('edit_tweet/<int:pk>', views.edit_tweet, name = "edit_tweet"),
    path('search', views.search, name = "search"),
    path('search_user', views.search_user, name = "search_user")
]