import logging

from django_filters import rest_framework as filters

from rooms.models import Room, Booking

logger = logging.getLogger('logger')


class RoomFilter(filters.FilterSet):

    price = filters.NumberFilter()
    price__gt = filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = filters.NumberFilter(field_name='price', lookup_expr='lt')
    capacity = filters.NumberFilter()
    capacity__gt = filters.NumberFilter(field_name='capacity', lookup_expr='gt')
    capacity__lt = filters.NumberFilter(field_name='capacity', lookup_expr='lt')

    order_by = filters.OrderingFilter(
        fields=(
            ('price', 'price'),
            ('capacity', 'capacity'),
        ),
    )

    avail_from = filters.ModelChoiceFilter(
        field_name='date_check_in',
        # lookup_expr='lt',
        queryset=Booking.objects.filter()
    )
    # avail_to = filters.DateFilter()

    # date_range = filters.DateFromToRangeFilter(
    # date_range = filters.DateRangeFilter(field_name='room__booking'
    #     # queryset=Room.objects.filter()
    # )

    class Meta:
        model = Room
        fields = [
            'price',
            'capacity',
            # 'room.booking__date_check_in',
            # 'room__booking__',
            # 'capacity',
        ]


# class BookingFilter(filters.FilterSet):
#
#     avail_from = filters.DateFilter(field_name='capacity', lookup_expr='lt')
#     avail_to = filters.DateFilter()
#     # date_range = filters.DateRangeFilter(
#     #     queryset=Room.objects.filter()
#     # )
#
#     class Meta:
#         model = Booking
#         fields = [
#             'date_check_in',
#             'date_check_out',
#             'room__name',
#         ]


# class BookingFilter(filters.FilterSet):
#
#     avail_from = filters.DateFilter(field_name='capacity', lookup_expr='lt')
#     avail_to = filters.DateFilter()
#     # date_range = filters.DateRangeFilter(
#     #     queryset=Room.objects.filter()
#     # )
#
#     class Meta:
#         model = Booking
#         fields = [
#             'date_check_in',
#             'date_check_out',
#             'room__name',
#         ]
