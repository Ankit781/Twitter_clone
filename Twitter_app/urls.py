from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login', views.loginuser ,name='loginuser'),
    path('logout', views.logoutuser, name='logoutuser'),
    path('', views.index, name='index'),
    path('profile_list/', views.profile_list, name = "profile_list"),
    path('profile/<int:pk>', views.profile, name= "profile")

]