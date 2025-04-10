from django.shortcuts import render
from .models import *
from .serializer import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.

class LoginView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer

class RegistrationStudentView(APIView):
    @swagger_auto_schema(
        request_body=Registration,    
        responses={
            200:openapi.Response('Registration Successfull....',Registration),
            400: 'Validation errors'
        }
    )
    def post(self,request):
        try:
            ser=Registration(data=request.data)
            if ser.is_valid():    
                user = ser.save()
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                return Response(data={"Status": "Success", "Msg": "Registration Successful!!!!", "data": ser.data,"tokens": {
                            "access": access_token,
                            "refresh": refresh_token
                        }}, status=status.HTTP_200_OK)
            else:
                return Response(data={"Status":"Failed","Msg":"Registration Unsuccessfull....","Errors":ser.errors},status=status.HTTP_400_BAD_REQUEST)  
        except Exception as e:
            return Response({"Status":"Failed","Error":str(e)},status=status.HTTP_400_BAD_REQUEST)
   
   
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self,request):
        try:
            user_id=request.user.id
            print(user_id)
            profile=CustomUser.objects.get(id=user_id)
            print(profile)
            ser=ProfileSer(profile)
            return Response(data={"Status":"Success","data":ser.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"Status":"Failed","Msg":str(e)},status=status.HTTP_404_NOT_FOUND)


class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    @swagger_auto_schema(
        request_body=ProfileSer,    
        responses={
            200:openapi.Response('Profile Updated....',ProfileSer),
            400: 'Validation errors'
        }
    )
    def put(self,request,**kwargs):
        # profile_id= kwargs.get('pk')
        try:
            profile=CustomUser.objects.get(id=request.user.id)
            ser=ProfileSer(profile,data=request.data,partial=True) 
            if ser.is_valid():
                ser.save()  
                return Response(data={"Status":"Success","Msg":"Profile updated successfully","data": ser.data},status=status.HTTP_200_OK)
            else:
                return Response(data={"Status": "Failed", "Msg": "Invalid data", "Errors": ser.errors},status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response(
                data={"Status": "Failed", "Msg": "Profile not found"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                data={"Status": "Failed", "Msg": str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        

class TripCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    @swagger_auto_schema(
        request_body=TripSerializer,
        responses={
            200:openapi.Response('Trip Added....',TripSerializer),
            400: 'Validation errors'
        }
    )
    def post(self,request):
        ser=TripSerializer(data=request.data,context={'request': request})
        if ser.is_valid():    
            ser.save()
            return Response(data={"Status": "Success", "Msg": "Product Added!!!!", "data": ser.data}, status=status.HTTP_200_OK)
        else:
            return Response(data={"Status":"Failed","Msg":"Something went wrong....","Errors":ser.errors},status=status.HTTP_400_BAD_REQUEST)  
   
   
class TripGetView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self,request):
        try:
            products=Trip.objects.filter(user=request.user)
            pro=TripSerializer(products,many=True)
            return Response(data={"Msg": "All Trips","data":pro.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"Msg": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
        
class TripUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    @swagger_auto_schema(
        request_body=TripSerializer,    
        responses={
            200:openapi.Response('Trip  Updated....',TripSerializer),
            400: 'Validation errors'
        })
    def put(self,request,**kwargs):
        product_id= kwargs.get('pk')
        try:
            product=Trip.objects.get(id=product_id)
            print(request.user)
            if product.user!=request.user:
                return Response(data={"Status":"Failed","Msg":"Unauthorized access: You do not have permission to modify this trip."},status=status.HTTP_401_UNAUTHORIZED)
            ser=TripSerializer(product,data=request.data,partial=True) 
            if ser.is_valid():
                ser.save()  
                return Response(data={"Status":"Success","Msg":"Trip updated successfully","data": ser.data},status=status.HTTP_200_OK)
            else:
                return Response(data={"Status": "Failed", "Msg": "Invalid data", "Errors": ser.errors},status=status.HTTP_400_BAD_REQUEST)
        except Trip.DoesNotExist:
            return Response(data={"Status": "Failed", "Msg": "Trip not found"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={"Status": "Failed", "Msg": str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TripDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def delete(self,request,**kwargs):
        try:
            product_id=kwargs.get('pk')
            product=Trip.objects.get(id=product_id)
            print(request.user)
            if product.user!=request.user:
                return Response(data={"Status":"Failed","Msg":"Unauthorized access: You do not have permission to delete this trip."},status=status.HTTP_401_UNAUTHORIZED)
            product.delete()
            return Response({"Status":"Success","Msg":f"{product.trip_name} Deleted Successfully!!!!!"})
        except Exception as e:
            return Response({"Status":"Failed","Error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

   
class AllTripsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self,request):
        try:
            products=Trip.objects.all()
            pro=TripSerializer(products,many=True)
            return Response(data={"Msg": "All Trips","data":pro.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"Msg": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
        
from rest_framework import viewsets
from .utils  import  get_or_create_personal_chat
from rest_framework.decorators import action


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]



class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all() 
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return ChatRoom.objects.filter(members__user=user).order_by('-created_at')
    
    def perform_create(self, serializer):
        room = serializer.save()
        RoomMember.objects.create(room=room, user=self.request.user, is_admin=True)
    
    @action(detail=False, methods=['get'])
    def my_chats(self, request):
        """Get all chats (both personal and group) for the current user"""
        user = request.user
        rooms = ChatRoom.objects.filter(members__user=user)
        serializer = self.get_serializer(rooms, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def start_personal_chat(self, request):
        """Start or get a personal chat with another user"""
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            other_user = CustomUser.objects.get(id=user_id)
            room = get_or_create_personal_chat(request.user, other_user)
            serializer = self.get_serializer(room)
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'], url_path='members/add')
    def add_member(self, request, pk=None):
        """Add a user to a group chat"""
        room = self.get_object()
        print("neww")
        if room.room_type != 'group':
            return Response({"error": "Can only add members to group chats"},status=status.HTTP_400_BAD_REQUEST)
        try:
            member = RoomMember.objects.get(room=room, user=request.user)
            if not member.is_admin:
                return Response({"error": "Only admins can add members"}, 
                                status=status.HTTP_403_FORBIDDEN)
            
        except RoomMember.DoesNotExist:
            return Response({"error": "You are not a member of this group"}, 
                            status=status.HTTP_403_FORBIDDEN)
        user_id = request.data.get('user_id')
        try:
            user = CustomUser.objects.get(id=user_id)
            RoomMember.objects.create(room=room, user=user)
            return Response({"status": "User added successfully"})
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    
from rest_framework.response import Response

class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        room_id = self.request.query_params.get('room_id')
        if not room_id:
            return Message.objects.none()
        user = self.request.user
        is_member = RoomMember.objects.filter(room_id=room_id, user=user).exists()
        if not is_member:
            return Message.objects.none()
        return Message.objects.filter(room_id=room_id).order_by('timestamp')

    @action(detail=False, methods=['post'])
    def send_message(self, request):
        """Handle sending a message"""
        room_id = self.request.query_params.get('room_id')
        content = request.data.get('content')

        if not room_id or not content:
            return Response({"error": "Room ID and message content are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        is_member = RoomMember.objects.filter(room_id=room_id, user=user).exists()
        if not is_member:
            return Response({"error": "User is not a member of this room."}, status=status.HTTP_403_FORBIDDEN)

        message = Message.objects.create(
            room_id=room_id,
            sender=user,
            content=content,
        )

        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Get count of unread messages grouped by room and sent messages"""
        user = request.user
        rooms = ChatRoom.objects.filter(members__user=user)
        result = []

        for room in rooms:
            unread_count = Message.objects.filter(
                room=room,
                sender__id=user.id,
                is_read=False
            ).count()

            sent_messages = Message.objects.filter(
                room=room,
                sender=user
            ).values('id', 'content', 'timestamp')  

            if unread_count > 0 or sent_messages.exists():
                result.append({
                    'room_id': room.id,
                    'room_name': room.name,
                    'unread_count': unread_count,
                    'sent_messages': list(sent_messages)  
                })
        return Response(result)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Mark a message as read"""
        try:
            message = Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            return Response({"error": "Message not found."}, status=status.HTTP_404_NOT_FOUND)

        if message.is_read:
            return Response({"message": "Message is already marked as read."}, status=status.HTTP_400_BAD_REQUEST)
        message.is_read = True
        message.save()

        return Response(MessageSerializer(message).data, status=status.HTTP_200_OK)
    
class MemberViewSet(viewsets.ModelViewSet):
    queryset = RoomMember.objects.all()
    serializer_class = RoomMemberSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        room_id = self.request.query_params.get('room_id')
        if room_id:
            return RoomMember.objects.filter(room_id=room_id)
        return RoomMember.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        room_id = self.request.data.get('room_id')
        user_id = self.request.data.get('user_id')
        
        try:
            room = ChatRoom.objects.get(id=room_id)
        except ChatRoom.DoesNotExist:
            raise ValidationError({"error": "Room not found"})
        
        if room.room_type != 'group':
            raise ValidationError({"error": "Can only add members to group chats"})
        
        try:
            current_user_member = RoomMember.objects.get(room=room, user=self.request.user)
            if not current_user_member.is_admin:
                raise ValidationError({"error": "Only admins can add members"})
        except RoomMember.DoesNotExist:
            raise ValidationError({"error": "You are not a member of this group"})
        
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise ValidationError({"error": "User not found"})
        
        if RoomMember.objects.filter(room=room, user=user).exists():
            raise ValidationError({"error": "User is already a member of this group"})
        serializer.save(room=room, user=user)
    
    @action(detail=False, methods=['delete'])
    def remove_member(self, request):
        """Remove a user from a group chat"""
        room_id = request.data.get('room_id')
        user_id = request.data.get('user_id')
        
        if not room_id or not user_id:
            return Response({"error": "room_id and user_id are required"}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        try:
            room = ChatRoom.objects.get(id=room_id)
            
            # Check if the room is a group chat
            if room.room_type != 'group':
                return Response({"error": "Can only remove members from group chats"},
                              status=status.HTTP_400_BAD_REQUEST)
            
            # Check if the current user is an admin
            try:
                current_user_member = RoomMember.objects.get(room=room, user=request.user)
                if not current_user_member.is_admin:
                    return Response({"error": "Only admins can remove members"}, 
                                  status=status.HTTP_403_FORBIDDEN)
            except RoomMember.DoesNotExist:
                return Response({"error": "You are not a member of this group"}, 
                              status=status.HTTP_403_FORBIDDEN)
            
            # Get the member to remove
            try:
                member = RoomMember.objects.get(room=room, user_id=user_id)
                # Don't allow removing the last admin
                if member.is_admin and RoomMember.objects.filter(room=room, is_admin=True).count() <= 1:
                    return Response({"error": "Cannot remove the last admin"}, 
                                  status=status.HTTP_400_BAD_REQUEST)
                member.delete()
                return Response({"status": "Member removed successfully"})
            except RoomMember.DoesNotExist:
                return Response({"error": "User is not a member of this group"}, 
                              status=status.HTTP_404_NOT_FOUND)
        except ChatRoom.DoesNotExist:
            return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def make_admin(self, request):
        """Make a user an admin of a group chat"""
        room_id = request.data.get('room_id')
        user_id = request.data.get('user_id')
        
        if not room_id or not user_id:
            return Response({"error": "room_id and user_id are required"}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        try:
            room = ChatRoom.objects.get(id=room_id)
            
            # Check if the room is a group chat
            if room.room_type != 'group':
                return Response({"error": "Can only set admins in group chats"},
                              status=status.HTTP_400_BAD_REQUEST)
            
            # Check if the current user is an admin
            try:
                current_user_member = RoomMember.objects.get(room=room, user=request.user)
                if not current_user_member.is_admin:
                    return Response({"error": "Only admins can set new admins"}, 
                                  status=status.HTTP_403_FORBIDDEN)
            except RoomMember.DoesNotExist:
                return Response({"error": "You are not a member of this group"}, 
                              status=status.HTTP_403_FORBIDDEN)
            
            # Get the member to promote
            try:
                member = RoomMember.objects.get(room=room, user_id=user_id)
                member.is_admin = True
                member.save()
                return Response({"status": "User is now an admin"})
            except RoomMember.DoesNotExist:
                return Response({"error": "User is not a member of this group"}, 
                              status=status.HTTP_404_NOT_FOUND)
        except ChatRoom.DoesNotExist:
            return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def list_members(self, request):
        """List all members of a room"""
        room_id = request.query_params.get('room_id')
        if not room_id:
            return Response({"error": "room_id is required"}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        try:
            room = ChatRoom.objects.get(id=room_id)
            
            # Check if the current user is a member
            if not RoomMember.objects.filter(room=room, user=request.user).exists():
                return Response({"error": "You are not a member of this room"}, 
                              status=status.HTTP_403_FORBIDDEN)
            
            members = RoomMember.objects.filter(room=room).select_related('user')
            member_data = []
            
            for member in members:
                member_data.append({
                    'id': member.id,
                    'user_id': member.user.id,
                    'username': member.user.name,
                    'is_admin': member.is_admin,
                    'joined_at': member.joined_at
                })
            
            return Response(member_data)
        except ChatRoom.DoesNotExist:
            return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)