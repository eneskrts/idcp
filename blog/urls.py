from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
from blog import views


urlpatterns = [
    path('blog_list/', views.PostListAPIView.as_view(), name='blog_list'),
    path('blog_detail/<int:pk>/', views.PostDetailAPIView.as_view(), name='blog_detail'),
]