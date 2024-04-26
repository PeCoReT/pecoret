from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import viewsets

app_name = 'asmonitor'

router = DefaultRouter()
router.register('programs', viewsets.ProgramViewSet, 'program')
router.register('tags', viewsets.TagViewSet, 'tag')
router.register('findings', viewsets.GlobalFindingList, 'finding')
router.register('targets', viewsets.GlobalTargetViewSet, 'target')

# all routes for programs
program_router = DefaultRouter()
program_router.register('targets', viewsets.TargetViewSet, 'target')
program_router.register('findings', viewsets.FindingViewSet, 'finding')

# all target related routes
target_router = DefaultRouter()
target_router.register('metas', viewsets.TargetMetaViewSet, 'meta')

urlpatterns = [
    path('asmonitor/', include(router.urls)),
    path('asmonitor/programs/<int:program>/', include((program_router.urls, 'asmonitor'), namespace='programs')),
    path('asmonitor/programs/<int:program>/targets/<int:target>/',
         include((target_router.urls, 'asmonitor'), namespace='targets'))

]
