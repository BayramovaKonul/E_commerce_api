from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):

    #Custom user model manager where email is the unique identifiers
    #for authentication instead of usernames.
    
    def create_user(self, email, first_name, last_name, password, **extra_fields):
        
        # Create and save a user with the given email and password.
       
        if not email:
            raise ValueError("The Email should be entered")
        if not first_name:
            raise ValueError("The First name should be entered")
        if not last_name:
            raise ValueError("The Last name should be entered")
        
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
   
        # Create and save a SuperUser with the given email and password.
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, first_name, last_name, password, **extra_fields)

class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=150, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        db_table = 'custom_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return "{} -> {} -> {}".format(self.email, self.first_name, self.last_name)
