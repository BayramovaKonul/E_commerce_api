from django.contrib import admin
from django.urls import path
from .views import CreateStoreView, UpdateStoreView, ListStoresView, StoreDashboardView, DeleteStoreView

urlpatterns = [
    path("create", CreateStoreView.as_view(), name="create_store"),
    path("update/<int:store_id>/", UpdateStoreView.as_view(), name="update_store"),
    path("", ListStoresView.as_view(), name="all_stores"),
    path("dashboard/<int:store_id>/", StoreDashboardView.as_view(), name="store_dashboard"),
    path("delete/<int:store_id>/", DeleteStoreView.as_view(), name="delete_store"),
]
