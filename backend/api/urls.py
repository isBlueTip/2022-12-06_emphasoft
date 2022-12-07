from django.urls import include, path
# from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
#                                    SpectacularSwaggerView)
# from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter

from api.rooms_views import BookingViewSet, RoomViewSet
from api.users_views import UserViewSet

app_name = 'api'

router = SimpleRouter()

router.register('users', UserViewSet, basename='user')
router.register('rooms', RoomViewSet, basename='room')
router.register('bookings', BookingViewSet, basename='booking')


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    # path('v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    # path('v1/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('v1/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
