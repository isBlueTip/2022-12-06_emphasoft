from django.contrib.auth.models import AbstractUser
from django.db import models
from django_paranoid.models import ParanoidModel


class User(AbstractUser, ParanoidModel):
    first_name = models.CharField(
        'first name',
        max_length=150,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        'last name',
        max_length=150,
        blank=True,
        null=True,
    )
    email = models.EmailField(
        'email address',
        blank=True,
    )
