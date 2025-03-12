from typing import Any, Dict
from rest_framework import serializers
from rest_framework_simplejwt.tokens import Token
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['id'] = user.id
        token['name'] = user.name
        token['email'] = user.email
        token['phone'] = user.phone
        token['image'] = user.image.url if user.image else None
        token['alternative_phone'] = user.alternative_phone if user.alternative_phone else None
        token['travel_type'] = user.travel_type if user.travel_type else None
        token['language'] = user.language if user.language else None
        token['id_proof'] = user.id_proof.url if user.id_proof else None  
        token['group_size'] = user.group_size if user.group_size else None  
        token['budget'] = user.budget if user.budget else None
        token['from_date'] = user.from_date if user.from_date else None
        token['to_date'] = user.to_date if user.to_date else None

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data['id'] = user.id
        data['name'] = user.name
        data['email'] = user.email
        data['phone'] = user.phone
        data['image'] = user.image.url if user.image else None
        data['alternative_phone'] = user.alternative_phone if user.alternative_phone else None
        data['travel_type'] = user.travel_type if user.travel_type else None
        data['language'] = user.language if user.language else None
        data['id_proof'] = user.id_proof.url if user.id_proof else None
        data['group_size'] = user.group_size if user.group_size else None
        data['budget'] = user.budget if user.budget else None
        data['from_date'] = user.from_date if user.from_date else None
        data['to_date'] = user.to_date if user.to_date else None
        
        return data
    
    
class Registration(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    id_proof = serializers.FileField(allow_null=True, required=False)  
    image = serializers.FileField(allow_null=True, required=False)  
    alternative_phone = serializers.IntegerField(required=False, allow_null=True, validators=[validate_phone])
    travel_type = serializers.CharField(required=False, allow_null=True)
    language = serializers.CharField(required=False, allow_null=True)
    budget = serializers.IntegerField(required=False, allow_null=True)
    from_date = serializers.DateField(required=False, allow_null=True)
    to_date = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'name', 'phone', 'email', 'password','image', 'alternative_phone', 'travel_type', 
            'language', 'id_proof', 'budget', 'from_date', 'to_date','group_size'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(**validated_data)  # This should be a method that hashes the password
        user.set_password(password)  # Ensure the password is hashed
        user.save()
        return user

    
    
class ProfileSer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model=CustomUser
        fields=['id','name', 'phone', 'email', 'alternative_phone','image', 'travel_type', 
            'language', 'id_proof', 'budget','group_size', 'from_date', 'to_date']
        
    def create(self,validated_data):
        return CustomUser.objects.create_user(**validated_data)
    
class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model=Trip
        fields=['id','name','description','price','stock','category','image_url','user']
        
      
 