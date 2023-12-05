from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login ,name='login'),
    path('logout', views.logoutuser, name='logout'),
    path('', views.index, name='index'),
    path('', views.google_logout, name='google_logout')
    # path('register', views.register, name="register"),
]