from chat.views import room
import json
from channels import auth
from django.contrib.auth import get_user_model
from django.core import paginator
from django.core.checks import messages
from django.core.paginator import Paginator
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Message, Room


User = get_user_model()

class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        room_name = self.scope['url_route']['kwargs']['room_name']
        roomMessages = Message.objects.filter(room = room_name).order_by('-timestamp')[:30]
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(roomMessages)
        }
        self.send_message(content)


    def new_message(self, data):
        author = data['from']
        room_name = self.scope['url_route']['kwargs']['room_name']
        author_user = User.objects.filter(username=author)[0]
        message = Message.objects.create(
                            author=author_user, 
                            room = room_name,
                            content=data['message'])
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)


    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'id': message.id,
            'author': message.author.username,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }
    
    commands = {
        "fetch_messages": fetch_messages,
        "new_message": new_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        return self.accept()

    def disconnect(self, code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    
    def send_read_receipts(self, message):
        username = message['author']
        message_id = message['id']
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_read_event',
                'from': username,
                'messageId': message_id
            }
        )
        
    def send_read_event(self, event):
        username = event['from']
        message_id = event['messageId']
        content = {
            'command': 'read_event',
            'from': username,
            'messageId': message_id
        }
        # Send message to WebSocket
        self.send(text_data=json.dumps(content))

    def send_chat_message(self, data):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': data
            }
        )
        user_id = self.scope["session"]["_auth_user_id"]
        current_user = User.objects.filter(id=user_id)[0]
        author = data['message']['author']
        if author is not current_user:
            self.send_read_receipts(data['message'])


    def send_message(self, message):
        self.send(text_data=json.dumps(message))
        

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))