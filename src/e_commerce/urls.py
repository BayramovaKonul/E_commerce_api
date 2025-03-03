from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('add-wishlist/<int:product_id>/', views.AddWishlistView.as_view(), name='add_wishlist'),
    path('delete-wishlist/<int:id>/', views.DeleteWishlistView.as_view(), name='delete_wishlist'),
    path('add-to-cart/<int:product_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
]