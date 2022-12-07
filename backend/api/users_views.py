from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.permissions import IsAuthenticatedOrReadOnlyOrRegister
from api.users_serializers import (CreateUserSerializer, PasswordSerializer,
                                   UserSerializer)
from users.models import User


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
    def set_user_password(self, request):
        user = self.request.user
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response(status=status.HTTP_201_CREATED)
