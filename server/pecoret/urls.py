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


