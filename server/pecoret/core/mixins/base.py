from rest_framework import mixins
from .filter import PeCoReTFilterBackendMixin


class ListModelMixin(mixins.ListModelMixin, PeCoReTFilterBackendMixin):
    pass


class UpdateModelMixin(mixins.UpdateModelMixin):
    pass


class RetrieveModelMixin(mixins.RetrieveModelMixin):
    pass


class CreateModelMixin(mixins.CreateModelMixin):
    pass


class DestroyModelMixin(mixins.DestroyModelMixin):
    pass
