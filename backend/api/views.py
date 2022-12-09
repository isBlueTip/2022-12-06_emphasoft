import logging

from api.filters import RoomFilter
from api.permissions import IsAdminOrCreate
from api.serializers import (
    BookingSerializer,
    CreateUserSerializer,
    RoomSerializer,
    UserSerializer,
)
from django.db.models.query import QuerySet
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rooms.models import Booking, Room
from users.models import User

logger = logging.getLogger('logger')


@extend_schema(tags=['Rooms'])
@extend_schema_view(
    list=extend_schema(
        summary='List all the rooms',
    ),
    retrieve=extend_schema(
        summary='Retrieve a room',
    ),
)
class RoomViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filterset_class = RoomFilter
    lookup_field = 'number'


@extend_schema(tags=['Bookings'])
@extend_schema_view(
    list=extend_schema(
        summary='List all the bookings',
    ),
    retrieve=extend_schema(
        summary='Retrieve booking',
    ),
)
class BookingViewSet(viewsets.ModelViewSet):

    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(guest=user)


@extend_schema(tags=['Users'])
@extend_schema_view(
    list=extend_schema(
        summary='List all the users',
    ),
    create=extend_schema(
        summary='Register new user',
    ),
    retrieve=extend_schema(
        summary='Retrieve user',
    ),
    update=extend_schema(
        summary='Update user info',
    ),
    partial_update=extend_schema(
        summary='Partially update user info',
    ),
    destroy=extend_schema(
        summary='Delete user',
    ),
)
class UserViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self) -> type(UserSerializer):
        if self.action == 'create':
            return CreateUserSerializer
        return UserSerializer

    queryset = User.objects.all()
    permission_classes = [IsAdminOrCreate]

    @extend_schema(tags=['Users'], summary='Info about current user')
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
