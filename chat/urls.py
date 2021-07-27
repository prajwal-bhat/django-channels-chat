from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
    path('api/chats/<str:room_name>/', views.get_chat_messages_paginated, name='room'),
]