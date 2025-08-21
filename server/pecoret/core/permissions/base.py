from rest_framework.permissions import BasePermission as DjangoBasePermission


class BasePermission(DjangoBasePermission):

    def __init__(self, *args, **kwargs):
        pass

    def has_permission(self, request, view):
        """
        ensure that we always check object permissions
        :param request:
        :param view:
        :return:
        """
        return self.has_object_permission(request, view, None)

    def __call__(self):
        # required because `permission_class` requires a class and not an instance
        return self
