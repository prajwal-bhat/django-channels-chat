from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()

# Model class to store the room info
class Room(models.Model):
    name = models.TextField()
    label = models.SlugField(unique=True)

    def __unicode__(self):
        return self.label

# Model class to store the messages
class Message(models.Model):
    room = models.TextField()
    author = models.ForeignKey(User, related_name="author_messages", on_delete=models.CASCADE)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username
