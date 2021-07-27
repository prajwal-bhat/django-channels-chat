from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import EmptyPage, Paginator
from chat.models import Message
from chat.serializers import MessageSerializer

from rest_framework.decorators import api_view
from rest_framework import status

import json



def index(request):
    return render(request, 'chat/index.html', {})


@login_required
def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
    })


@api_view(['GET'])
def get_chat_messages_paginated(request, room_name, pk):
    # GET all published tutorials
    page_size = 30
    messagesObj = Message.objects.order_by('-timestamp').all()
    paginator = Paginator(messagesObj, page_size)
    try:
        messages = paginator.page(pk)
    except EmptyPage:
        messages = paginator.page(1)
    if request.method == "GET":
        messages_serialized = MessageSerializer(messages, many=True)
        return JsonResponse(messages_serialized.data, safe=False)