from django.urls import include, path


app_name = "api"


urlpatterns = [
    path('', include('backend.api.urls')),
    path('', include('checklists.urls')),
    path('', include('advisories.urls')),
    path('', include('attack_surface.urls')),
    path('', include('core.webhooks.urls')),
]

