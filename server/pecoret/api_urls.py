from django.urls import include, path
from django.conf import settings


app_name = "api"


urlpatterns = [
    path('', include('backend.api.urls')),
    path('', include('checklists.urls')),
    path('', include('advisories.urls')),
    path('', include('attack_surface.urls'))
]


if settings.DEBUG:
    from drf_spectacular.views import SpectacularRedocView, SpectacularAPIView

    urlpatterns += [
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]
