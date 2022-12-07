from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, BasePermission,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from api.permissions import IsAuthor
from api.rooms_serializers import RoomSerializer, BookingSerializer
from rooms.models import Room, Booking


class RoomViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]


class BookingViewSet(viewsets.ModelViewSet):

    queryset = Booking.objects.all()
    pagination_class = None
    serializer_class = BookingSerializer
    permission_classes = [IsAuthor]
