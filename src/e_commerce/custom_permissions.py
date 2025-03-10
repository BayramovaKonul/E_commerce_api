from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow users to edit or delete their own wishlist.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user is the owner of the wishlist
        return obj.user == request.user


class IsOrderItemStoreOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only the store owner to change the product status.
    Others have read-only access.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow editing only if the user is the owner of the product's store
        return obj.product.store.owner == request.user