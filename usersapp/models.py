from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
#from moviematchapp.models import Movie # Step 10

# Create your models here.
# Step 1: define custom User model and manager and set AUTH_USER_MODEL = "usersapp.User" in settings.py then create the login template with all folders templates/registration/

class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("Email shoudn't be empty")
        if not password:
            raise ValueError("Password shoudn't be empty")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=200)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "password"]
    objects = UserManager()

    def __str__(self):
        return self.name
    class Meta:
        db_table = "users"
        managed = False

