from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import viewsets


app_name = 'asmonitor'


router = DefaultRouter()
router.register('programs', viewsets.ProgramViewSet, 'program')
router.register('tags', viewsets.TagViewSet, 'tag')
router.register('findings', viewsets.GlobalFindingList, 'finding')

# all routes for programs
program_router = DefaultRouter()
program_router.register('targets', viewsets.TargetViewSet, 'target')
program_router.register('findings', viewsets.FindingViewSet, 'finding')

urlpatterns = [
    path('asmonitor/', include(router.urls)),
    path('asmonitor/programs/<int:program>/', include(program_router.urls))
]
