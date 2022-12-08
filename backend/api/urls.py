from django.urls import include, path
from drf_spectacular.views import SpectacularRedocView, SpectacularSwaggerView
from rest_framework.routers import SimpleRouter

from api.views import BookingViewSet, RoomViewSet, UserViewSet

app_name = 'api'

router = SimpleRouter()

router.register('users', UserViewSet, basename='user')
router.register('rooms', RoomViewSet, basename='room')
router.register('bookings', BookingViewSet, basename='booking')


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    path(
        'docs/swagger/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    path(
        'docs/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
]
