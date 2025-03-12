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