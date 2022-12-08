from decimal import Decimal

from django.core import validators
from django.db import models
from users.models import User


class Room(models.Model):
    number = models.PositiveIntegerField(
        unique=True,
        verbose_name='Room number',
    )
    name = models.CharField(
        unique=True,
        max_length=64,
        verbose_name='Room name',
    )
    price = models.DecimalField(
        db_index=True,
        max_digits=16,
        decimal_places=2,
        validators=[validators.MinValueValidator(Decimal('0'))],
        verbose_name='Price per night',
    )
    capacity = models.PositiveIntegerField(
        db_index=True,
        verbose_name='Max number of guests',
    )

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f'{self.number} - {self.name}'


class Booking(models.Model):
    room = models.ForeignKey(
        Room,
        related_name='bookings',
        on_delete=models.CASCADE,
        verbose_name='Room',
    )
    guest = models.ForeignKey(
        User,
        related_name='bookings',
        on_delete=models.CASCADE,
        verbose_name='Guest',
    )
    date_check_in = models.DateField(
        db_index=True, verbose_name='Check-in date'
    )
    date_check_out = models.DateField(
        db_index=True, verbose_name='Check-out date'
    )

    class Meta:
        ordering = ['date_check_in']

    def __str__(self):
        return f'{self.room} - {self.date_check_in} : {self.date_check_out}'
