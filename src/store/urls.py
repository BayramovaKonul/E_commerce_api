from django.contrib import admin
from django.urls import path
from .views import CreateStoreView, UpdateStoreView, ListStoresView

urlpatterns = [
    path("create", CreateStoreView.as_view(), name="create_store"),
    path("update/<int:store_id>/", UpdateStoreView.as_view(), name="update_store"),
    path("", ListStoresView.as_view(), name="all_stores"),
]
