import logging

from django_filters import rest_framework as filters
from rooms.models import Room

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

    class Meta:
        model = Room
        fields = [
            'price',
            'capacity',
        ]
