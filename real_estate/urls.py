# real_estate/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import homepage, contact


urlpatterns = [
    path('admin/', admin.site.urls),
    path('listings/', include('listings.urls')),
    path('accounts/', include('accounts.urls')),
    path('orders/', include('orders.urls')),  # Include orders URLs
    path('contact/', contact, name='contact'),
    path('', homepage, name='homepage'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)