from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import timedelta
from django.utils import timezone
from .validators import *
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None , **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone=models.BigIntegerField(unique=True,validators=[validate_phone])
    image =  models.FileField(upload_to="profile_image",null=True,blank=True)
    group_size = models.IntegerField(null=True,blank=True)
    alternative_phone = models.BigIntegerField(validators=[validate_phone],null=True,blank=True)
    travel_type = models.CharField(max_length=200,null=True,blank=True)
    language =  models.CharField(max_length=200,null=True,blank=True)
    id_proof = models.FileField(upload_to="id_proof",null=True,blank=True)
    budget = models.IntegerField(null=True,blank=True)
    from_date = models.DateField(null=True,blank=True)
    to_date = models.DateField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','phone']

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def _str_(self):
        return self.email


class Trip(models.Model):
    trip_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    travel_type = models.CharField(max_length=200)
    group_size = models.IntegerField()
    budget = models.IntegerField()
    from_date = models.DateField()
    to_date = models.DateField()
    image = models.FileField(upload_to="trip_image")
    
    def __str__(self):
        return self.trip_name