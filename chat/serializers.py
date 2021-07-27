from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):


    class Meta:
        model = Message
        fields = ('id', 'author', 'content', 'timestamp')