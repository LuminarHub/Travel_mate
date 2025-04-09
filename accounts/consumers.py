# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Message, ChatRoom, RoomMember,CustomUser

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        
        # Get the user from the scope (requires authentication)
        self.user = self.scope['user']
        
        # Check if user is a member of this room
        is_member = await self.is_room_member(self.user.id, self.room_id)
        if not is_member:
            # Reject the connection if not a member
            await self.close()
            return
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
        # Mark unread messages as read when user connects
        await self.mark_messages_as_read(self.user.id, self.room_id)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']

        # Get room details
        room = await self.get_room(self.room_id)
        
        # Save message to the database
        message = await self.save_message(self.user.id, message_content, self.room_id)

        # Send message to room group (broadcast the message to others)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',  # WebSocket event type to send
                'message': message_content,
                'username': self.user.username,
                'user_id': self.user.id,
                'message_id': message.id,
                'timestamp': message.timestamp.isoformat(),
                'room_type': room.room_type
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
            'user_id': event['user_id'],
            'message_id': event['message_id'],
            'timestamp': event['timestamp'],
            'room_type': event['room_type']
        }))

    
    @database_sync_to_async
    def is_room_member(self, user_id, room_id):
        try:
            return RoomMember.objects.filter(user_id=user_id, room_id=room_id).exists()
        except:
            return False
    
    @database_sync_to_async
    def get_room(self, room_id):
        return ChatRoom.objects.get(id=room_id)
    
    @database_sync_to_async
    def save_message(self, user_id, content, room_id):
        user = User.objects.get(id=user_id)
        room = ChatRoom.objects.get(id=room_id)
        message = Message.objects.create(
            sender=user,
            content=content,
            room=room
        )
        return message
    
    @database_sync_to_async
    def mark_messages_as_read(self, user_id, room_id):
        Message.objects.filter(
            room_id=room_id,
            sender__id__ne=user_id,
            is_read=False
        ).update(is_read=True)
        
    # Receive message from WebSocket

    @database_sync_to_async
    def save_message(self, user_id, content, room_id):
        user = CustomUser.objects.get(id=user_id)  # Use CustomUser instead of User
        room = ChatRoom.objects.get(id=room_id)
        
        message = Message.objects.create(
            sender=user,  # Ensure it's a CustomUser instance
            content=content,
            room=room
        )
        return message
