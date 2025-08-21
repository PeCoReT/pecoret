from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework as filters
from . import mixins as p_mixins


class PeCoReTModelViewSet(p_mixins.PeCoReTFilterBackendMixin, viewsets.ModelViewSet):
    pass


class PeCoReTNoDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    p_mixins.PeCoReTFilterBackendMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    pass


class PeCoReTNoUpdateViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]


class PeCoReTReadOnlyModelViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]


class PeCoReTListUpdateRetrieveModelViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    pass


class GenericViewSet(viewsets.GenericViewSet):
    pass


class ModelViewSet(p_mixins.RetrieveModelMixin, p_mixins.UpdateModelMixin, p_mixins.ListModelMixin,
                   p_mixins.CreateModelMixin, p_mixins.DestroyModelMixin,
                   p_mixins.PeCoReTFilterBackendMixin,
                   GenericViewSet):
    pass
