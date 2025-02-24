from rest_framework import permissions

class IsProductOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow store owners to edit or delete their product.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the product belongs to a store and if the user is the owner of that store
        product_store = obj.store 

        # Check if the user is the owner of the store
        return product_store.owner == request.user
