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
from .utils import get_or_create_personal_chat
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
        return ChatRoom.objects.filter(members__user=user)
    
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
    
    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        """Add a user to a group chat"""
        room = self.get_object()
        if room.room_type != 'group':
            return Response({"error": "Can only add members to group chats"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
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
    
class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Message.objects.all() 
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        room_id = self.request.query_params.get('room_id')
        if not room_id:
            return Message.objects.none()
        
        user = self.request.user
        # Check if the user is a member of this room
        is_member = RoomMember.objects.filter(room_id=room_id, user=user).exists()
        if not is_member:
            return Message.objects.none()
        
        # Return messages for this room
        return Message.objects.filter(room_id=room_id).order_by('timestamp')
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Get count of unread messages grouped by room"""
        user = request.user
        # Get rooms where user is a member
        rooms = ChatRoom.objects.filter(members__user=user)
        result = []
        
        for room in rooms:
            unread_count = Message.objects.filter(
                room=room, 
                sender__id__ne=user.id, 
                is_read=False
            ).count()
            
            if unread_count > 0:
                result.append({
                    'room_id': room.id,
                    'room_name': room.name,
                    'unread_count': unread_count
                })
                
        return Response(result)