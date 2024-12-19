from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.store')),
    path('api/', include('apps.cart')),
    path('api/', include('apps.payments')),
    path('api/', include('apps.authentication')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
