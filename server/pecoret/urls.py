from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('backend.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('pecoret.api_urls'), name='api'),

    # TODO: migrate to api
    path("accounts/", include("allauth.urls")),
    path("api/_allauth/", include("allauth.headless.urls"))
]



if settings.DEBUG:
    from drf_spectacular.views import SpectacularRedocView, SpectacularAPIView

    urlpatterns += [
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]
