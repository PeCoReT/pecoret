from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path('api/', include('backend.urls')),
    path('api/', include('checklists.urls')),
    path('api/', include('advisories.urls')),
    path('api/', include('attack_surface.urls')),
]

if settings.DEBUG:
    from drf_spectacular.views import SpectacularRedocView, SpectacularAPIView, SpectacularSwaggerView

    urlpatterns += [
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
        path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    ]
