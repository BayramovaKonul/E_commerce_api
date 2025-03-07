from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('add-wishlist/<int:product_id>/', views.AddWishlistView.as_view(), name='add_wishlist'),
    path('delete-wishlist/<int:wishlist_id>/', views.DeleteWishlistView.as_view(), name='delete_wishlist'),
    path('my-wishlist', views.MyWishListView.as_view(), name='my_wishlist'),
    path('add-to-cart/<int:product_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('delete-cart/<int:cart_id>/', views.DeleteFromCartView.as_view(), name='delete_cart'),
    path('my-cart', views.MyCartView.as_view(), name='my_cart'),
    path('update-cart/<int:cart_id>/', views.UpdateCartAPIView.as_view(), name='update_cart'),
]