from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
