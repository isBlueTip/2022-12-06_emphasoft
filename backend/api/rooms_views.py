import logging
from http import HTTPStatus

from api.filters import RoomFilter
from api.permissions import IsAdminOrCreate, IsAdminOrReadOnly  # , IsAuthor
from api.rooms_serializers import BookingSerializer, RoomSerializer
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response
from rooms.models import Booking, Room

logger = logging.getLogger('logger')


class RoomViewSet(viewsets.ModelViewSet):

    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = RoomFilter
    lookup_url_kwargs = ['checkin_date', 'checkout_date']

    def validate(self):
        checkin_date = self.request.query_params.get('checkin_date')
        logger.debug(checkin_date)
        logger.debug(checkin_date)
        pass

    def list(self, request, *args, **kwargs):
        checkin_date = request.query_params.get('checkin_date')
        checkout_date = request.query_params.get('checkout_date')
        if checkin_date and checkout_date:
            # logger.debug(checkin_date)
            queryset = Room.objects.exclude(
                Q(
                    bookings__date_check_in__lte=checkin_date,
                    bookings__date_check_out__gt=checkin_date,
                )
                | Q(
                    bookings__date_check_in__lt=checkout_date,
                    bookings__date_check_out__gte=checkout_date,
                )
            )
            # logger.debug(queryset)
        elif checkin_date:
            return Response(
                data='You have to provide checkout_date',
                status=HTTPStatus.BAD_REQUEST,
            )
        elif checkout_date:
            return Response(
                data='You have to provide checkin_date',
                status=HTTPStatus.BAD_REQUEST,
            )
        else:
            queryset = Room.objects.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BookingViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(guest=user)

    pagination_class = None  # TODO which pagination?
    serializer_class = BookingSerializer
    permission_classes = [IsAdminOrCreate]
