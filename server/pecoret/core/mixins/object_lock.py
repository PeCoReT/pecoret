from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.models.object_lock import ObjectLock


class ObjectLockMixin:
    """
    the queryset model must implement a property `object_lock_instance` that holds the ``ObjectLock`` related object
    """

    @action(detail=True, methods=['post'])
    def lock(self, request, *args, **kwargs):
        obj = self.get_object()
        locked_object = obj.object_lock_instance
        if locked_object and locked_object.user.pk != request.user.pk:
            response = Response({'detail': 'already locked'}, status=status.HTTP_400_BAD_REQUEST)
            return response
        if locked_object and locked_object.user.pk == request.user.pk:
            locked_object.save()
            serializer = self.get_serializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        ObjectLock.objects.create(user=request.user, locked_object=obj)
        serializer = self.get_serializer(obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
    def unlock(self, request, *args, **kwargs):
        obj = self.get_object()
        locked_object = obj.object_lock_instance
        if not locked_object:
            return Response({'detail': 'not locked'}, status=status.HTTP_400_BAD_REQUEST)
        if request.user.pk == locked_object.user.pk:
            locked_object.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'locked by another user'}, status=status.HTTP_400_BAD_REQUEST)
