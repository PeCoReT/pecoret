from django.urls import path, include

urlpatterns = [
    path('', include('backend.urls')),
    path('api/', include('pecoret.api_urls'), name='api'),
]


