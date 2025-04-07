# utils.py
from django.contrib.auth.models import User
from .models import ChatRoom, RoomMember

def get_or_create_personal_chat(user1, user2):
    """
    Get or create a personal chat room between two users.
    The room name is created using both user IDs in sorted order to ensure consistency.
    """
    user_ids = sorted([user1.id, user2.id])
    room_name = f"personal_{user_ids[0]}_{user_ids[1]}"
    
    try:
        room = ChatRoom.objects.get(name=room_name, room_type='personal')
    except ChatRoom.DoesNotExist:
        room = ChatRoom.objects.create(name=room_name, room_type='personal')
        
        RoomMember.objects.create(room=room, user=user1)
        RoomMember.objects.create(room=room, user=user2)
    
    return room