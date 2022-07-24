from django.contrib import admin
from django.urls import path, include
from .views import MyLoginView
from django.contrib.auth.views import LogoutView

app_name = 'user'

urlpatterns = [
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
