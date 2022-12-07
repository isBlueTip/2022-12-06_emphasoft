import logging

from datetime import date

from rest_framework import serializers, status
from rest_framework.response import Response
from rooms.models import Room, Booking
from collections import namedtuple
Range = namedtuple('Range', ['start', 'end'])

logger = logging.getLogger('logger')


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = [
            'number',
            'name',
            'price',
            'capacity',
        ]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'room',
            'guest',
            'date_check_in',
            'date_check_out',
        ]

        read_only_fields = [
            'guest'
        ]

    def validate(self, data):
        requested_check_in = data.get('date_check_in')
        requested_check_out = data.get('date_check_out')
        if requested_check_in < date.today():
            raise serializers.ValidationError(
                'You can\'t book earlier than today')

        if requested_check_in >= requested_check_out:
            raise serializers.ValidationError(
                'Check-in date must be earlier than check-out date')
        bookings = Booking.objects.filter(room=data['room'])

        for booking in bookings:  # check if requested dates are available
            r1 = Range(booking.date_check_in, booking.date_check_out)
            r2 = Range(requested_check_in, requested_check_out)
            latest_start = max(r1.start, r2.start)
            earliest_end = min(r1.end, r2.end)
            logger.debug(r1.start)
            logger.debug(r1.end)
            logger.debug(r2.start)
            logger.debug(r2.end)
            delta = (latest_start - earliest_end).days
            if delta < 0:
                raise serializers.ValidationError(
                    'Sorry, the room is not available for the given dates')
        return data

    def create(self, validated_data):
        user = self.context.get('request').user
        room = validated_data['room']
        requested_check_in = validated_data['date_check_in']
        requested_check_out = validated_data['date_check_out']
        booking = Booking.objects.create(
            room=room,
            guest=user,
            date_check_in=requested_check_in,
            date_check_out=requested_check_out
        )
        return booking
