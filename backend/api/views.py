import logging

from django.db.models.query import QuerySet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.filters import RoomFilter
from api.permissions import IsAdminOrCreate, IsAdminOrReadOnly
from api.serializers import (
    BookingSerializer,
    CreateUserSerializer,
    RoomSerializer,
    UserSerializer,
)
from rooms.models import Booking, Room
from users.models import User

logger = logging.getLogger('logger')


class RoomViewSet(viewsets.ModelViewSet):

    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = RoomFilter
    lookup_field = 'number'


class BookingViewSet(viewsets.ModelViewSet):

    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(guest=user)


class UserViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self) -> type(UserSerializer):
        if self.action == 'create':
            return CreateUserSerializer
        return UserSerializer

    queryset = User.objects.all()
    permission_classes = [IsAdminOrCreate]

    @action(  # user info about self
        detail=False,
        methods=[
            'get',
        ],
        permission_classes=[
            IsAuthenticated,
        ],
        url_path='me',
        url_name='me',
        name='View current user details',
    )
    def view_user_info(self, request: Request) -> Response:
        user = self.request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
