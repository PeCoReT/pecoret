from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import viewsets

app_name = 'asmonitor'

router = DefaultRouter()
router.register('programs', viewsets.ProgramViewSet, 'program')
router.register('tags', viewsets.TagViewSet, 'tag')
router.register('findings', viewsets.GlobalFindingList, 'finding')
router.register('targets', viewsets.GlobalTargetViewSet, 'target')
router.register('urls', viewsets.GlobalURLViewSet, 'url')
router.register('ports', viewsets.GlobalPortViewSet, 'port')


# all routes for programs
program_router = DefaultRouter()
program_router.register('targets', viewsets.TargetViewSet, 'target')
program_router.register('findings', viewsets.FindingViewSet, 'finding')
program_router.register('scopes', viewsets.ScopeViewSet, 'scope')


# all target related routes
host_router = DefaultRouter()
host_router.register('metas', viewsets.TargetMetaViewSet, 'meta')
host_router.register('urls', viewsets.URLViewSet, 'url')
host_router.register('ports', viewsets.PortViewSet, 'port')


urlpatterns = [
    path('asmonitor/', include(router.urls)),
    path('asmonitor/programs/<int:program>/', include((program_router.urls, 'asmonitor'), namespace='programs')),
    path('asmonitor/programs/<int:program>/targets/<int:target>/',
         include((host_router.urls, 'asmonitor'), namespace='targets'))
]
