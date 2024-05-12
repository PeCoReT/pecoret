from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import viewsets

app_name = 'asmonitor'

router = DefaultRouter()
router.register('programs', viewsets.ProgramViewSet, 'program')
router.register('tags', viewsets.TagViewSet, 'tag')
router.register('findings', viewsets.GlobalFindingList, 'finding')
router.register('hosts', viewsets.GlobalHostViewSet, 'host')
router.register('urls', viewsets.GlobalURLViewSet, 'url')


# all routes for programs
program_router = DefaultRouter()
program_router.register('hosts', viewsets.HostViewSet, 'host')
program_router.register('findings', viewsets.FindingViewSet, 'finding')
program_router.register('scopes', viewsets.ScopeViewSet, 'scope')


# all target related routes
host_router = DefaultRouter()
host_router.register('metas', viewsets.TargetMetaViewSet, 'meta')
host_router.register('hostnames', viewsets.HostnameViewSet, 'hostname')
host_router.register('urls', viewsets.URLViewSet, 'url')
host_router.register('ports', viewsets.PortViewSet, 'port')


urlpatterns = [
    path('asmonitor/', include(router.urls)),
    path('asmonitor/programs/<int:program>/', include((program_router.urls, 'asmonitor'), namespace='programs')),
    path('asmonitor/programs/<int:program>/hosts/<int:host>/',
         include((host_router.urls, 'asmonitor'), namespace='hosts'))
]
