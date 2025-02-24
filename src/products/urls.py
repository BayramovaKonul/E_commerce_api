from django.contrib import admin
from django.urls import path
from .views import AddProductView, DeleteProductView, UpdateProductView

urlpatterns = [
    path("add", AddProductView.as_view(), name="add_product"),
    path("delete/<int:product_id>/", DeleteProductView.as_view(), name="delete_product"),
    path("update/<int:product_id>/", UpdateProductView.as_view(), name="update_product"),
]
