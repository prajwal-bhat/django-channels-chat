from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login/', views.redirect_to_admin_page, name="home"),
    path('chat/', views.redirect_to_admin_page, name="home"),
    path('chat/<str:room_name>/', views.room, name='room'),
    path('api/chats/<str:room_name>/<int:pk>/', views.get_chat_messages_paginated, name='chats'),
]