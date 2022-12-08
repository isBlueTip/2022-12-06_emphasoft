import logging
from datetime import date

from django.db.models import Q
from django.db.models.query import QuerySet
from django_filters import rest_framework as filters
from rest_framework import serializers

from rooms.models import Room

logger = logging.getLogger('logger')


class RoomFilter(filters.FilterSet):

    price = filters.NumberFilter()
    price_min = filters.NumberFilter(field_name='price', lookup_expr='gt')
    price_max = filters.NumberFilter(field_name='price', lookup_expr='lt')
    capacity = filters.NumberFilter()
    capacity_min = filters.NumberFilter(
        field_name='capacity', lookup_expr='gt'
    )
    capacity_max = filters.NumberFilter(
        field_name='capacity', lookup_expr='lt'
    )

    order_by = filters.OrderingFilter(
        fields=(
            ('price', 'price'),
            ('capacity', 'capacity'),
        ),
    )

    date_range = filters.DateFromToRangeFilter(method='filter_requested_dates')

    def filter_requested_dates(
        self, queryset: QuerySet, name: str, value: slice
    ) -> QuerySet:
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
