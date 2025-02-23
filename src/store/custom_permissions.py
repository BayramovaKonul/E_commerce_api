from rest_framework import permissions

class IsStoreOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow store owners to edit their store.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user is the owner of the store
        return obj.owner == request.user
