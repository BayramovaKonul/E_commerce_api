from rest_framework import permissions

class IsWishlistOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow users to edit or delete their own wishlist.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user is the owner of the wishlist
        return obj.user == request.user
