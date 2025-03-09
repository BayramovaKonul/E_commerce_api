from django.contrib import admin
from django.urls import path, include
from . import views
from .views import MyWishListView

urlpatterns = [
    path('wishlist/<int:wishlist_id>/', views.DeleteWishlistView.as_view(), name='delete_wishlist'),
    path('wishlist/', MyWishListView.as_view(), name='list_add_wishlist'),  # For GET and POST requests
    path('cart', views.MyCartView.as_view(), name='list_add_cart'),  # for GET and POST requests
    path('cart/<int:cart_id>/', views.DetailCartAPIView.as_view(), name='update_delete_cart'), # DELETE and PUT requests
]
