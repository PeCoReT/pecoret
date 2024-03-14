from django.contrib import admin
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path('api/', include('backend.urls')),
    path('api/', include('checklists.urls')),
    path('api/', include('advisories.urls')),
    path('api/', include('asmonitor.urls'))
]

if settings.DEBUG:
    from drf_spectacular.views import SpectacularRedocView, SpectacularAPIView

    urlpatterns += [
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]

if settings.ENABLE_DJANGO_ADMIN_PANEL:
    urlpatterns += [
        path('api/admin/', admin.site.urls),
    ]
