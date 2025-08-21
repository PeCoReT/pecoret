from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import viewsets


app_name = "checklists"

router = DefaultRouter()

router.register("checklists", viewsets.ChecklistViewSet, "checklist")
router.register('categories', viewsets.CategoryViewSet, 'category')
router.register('items', viewsets.ItemViewSet, 'item')

project_router = DefaultRouter()
project_router.register("checklists", viewsets.AssetChecklistViewSet, "checklist")
project_router.register("checklist-categories", viewsets.AssetCategoryViewSet, "checklist-category")
project_router.register("checklist-items", viewsets.AssetItemViewSet, "checklist-item")


urlpatterns = [
    path("projects/<int:project>/", include((project_router.urls, "checklists"), namespace="projects")),
    path("checks/", include(router.urls)),
]
