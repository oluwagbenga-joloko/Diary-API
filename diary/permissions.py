from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, instance):
        if request.user.is_superuser:
            return True
        return request.user.id == instance.user_id
        