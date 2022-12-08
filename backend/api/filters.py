import logging

from django_filters import rest_framework as filters
from rooms.models import Room
from rest_framework import serializers
from datetime import date

# from django_filters.rest_framework import BooleanWidget

from django.db.models import Q

logger = logging.getLogger('logger')


class RoomFilter(filters.FilterSet):

    price = filters.NumberFilter()
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gt')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lt')
    capacity = filters.NumberFilter()
    min_capacity = filters.NumberFilter(
        field_name='capacity', lookup_expr='gt'
    )
    max_capacity = filters.NumberFilter(
        field_name='capacity', lookup_expr='lt'
    )

    order_by = filters.OrderingFilter(
        fields=(
            ('price', 'price'),
            ('capacity', 'capacity'),
        ),
    )

    date_range = filters.DateFromToRangeFilter(method='filter_requested_dates')

    def filter_requested_dates(self, queryset, name, value):
        logger.debug(value)
        try:
            checkin_date = value.start.date()
            checkout_date = value.stop.date()
        except AttributeError:
            raise serializers.ValidationError(
                'You must provide both check-in'
                ' and check-out dates, for example:'
                '/api/rooms/?date_range_after=2022-12-10'
                '&date_range_before=2022-12-14'
            )
        if checkin_date < date.today():
            raise serializers.ValidationError('You can\'t look for past dates')
        if checkin_date > checkout_date:
            raise serializers.ValidationError(
                'Check-in date must be earlier than check-out date'
            )
        elif checkin_date == checkout_date:
            raise serializers.ValidationError('Select at least one night')
        queryset = Room.objects.exclude(
            Q(
                bookings__date_check_in__gte=checkin_date,
                bookings__date_check_in__lt=checkout_date,
            )
            | Q(
                bookings__date_check_out__gt=checkin_date,
                bookings__date_check_out__lte=checkout_date,
            )
        )
        return queryset

    class Meta:
        model = Room
        fields = [
            'price',
            'capacity',
        ]
