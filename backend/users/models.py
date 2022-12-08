from django_paranoid.models import ParanoidModel

# from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth import get_user_model


# class User(AbstractUser, ParanoidModel):
#     field = models.CharField(max_length=20)

User = get_user_model()
