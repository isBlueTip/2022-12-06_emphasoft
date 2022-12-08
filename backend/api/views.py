import logging
from http import HTTPStatus
from datetime import date, datetime

from api.filters import RoomFilter
from api.permissions import IsAdminOrReadOnly  # , IsAuthor
from api.permissions import (
    IsAdminOrCreate,
    IsAuthenticatedOrReadOnlyOrRegister,
)
from api.serializers import BookingSerializer, RoomSerializer
from api.serializers import (
    CreateUserSerializer,
    PasswordSerializer,
    UserSerializer,
)
from rest_framework import status, viewsets, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rooms.models import Booking, Room
from users.models import User

logger = logging.getLogger('logger')


class RoomViewSet(viewsets.ModelViewSet):

    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = RoomFilter


class BookingViewSet(viewsets.ModelViewSet):

    serializer_class = BookingSerializer
    permission_classes = [IsAdminOrCreate]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(guest=user)


class UserViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        return UserSerializer

    queryset = User.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnlyOrRegister]

    @action(
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
    def view_user_info(self, request):
        user = self.request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=[
            'post',
        ],
        permission_classes=[
            IsAuthenticated,
        ],
        serializer_class=PasswordSerializer,
        url_path='set_password',
        name='Change current user password',
    )
    def set_user_password(self, request) -> Response:
        user = self.request.user
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response(status=status.HTTP_201_CREATED)
