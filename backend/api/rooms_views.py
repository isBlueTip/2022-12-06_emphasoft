import logging

from rest_framework import viewsets

from api.permissions import IsAdminOrCreate, IsAdminOrReadOnly  # , IsAuthor
from api.rooms_serializers import BookingSerializer, RoomSerializer
from rooms.models import Booking, Room

logger = logging.getLogger('logger')


class RoomViewSet(viewsets.ModelViewSet):

    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]


class BookingViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(guest=user)

    pagination_class = None  # TODO which pagination?
    serializer_class = BookingSerializer
    permission_classes = [IsAdminOrCreate]

    # @action(
    #     detail=False,
    #     methods=[
    #         "get",
    #         "delete",
    #     ],
    #     serializer_class=BookingSerializer,
    #     permission_classes=[IsAuthor,]
    # )
    # def my_bookings(self, request,*args, **kwargs):
    #     queryset = self.get_queryset()
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)
