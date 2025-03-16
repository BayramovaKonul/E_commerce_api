import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from tests.confest import user, authenticated_client, product, address, store, category, order, order_detail, another_user, another_authenticated_client, product2
from django.urls import reverse

@pytest.mark.django_db
class TestStoreOrderHistoryView:
    
    def test_store_order_history_for_non_owner(self, another_authenticated_client, store):
        """Test that a user who is not the owner cannot view the order history"""

        url = reverse("order_history", args=[store.id])

        response = another_authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN, f"Expected 403, got {response.status_code}"


    def test_store_not_found(self, store, authenticated_client):
        """Test that an owner cannot view order history when a store is not found"""

        url = reverse("order_history", args=(9999,))

        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['error'] == "Store not found"


    def test_store_order_history_valid_store(self, authenticated_client, store, order, order_detail):
        """
        Test retrieving order history for a valid store.
        """
        url = reverse("order_history", args=[store.id])
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "order_data" in data
        assert len(data["order_data"]) == 1
        assert data["order_data"][0]["order_id"] == order.id
        assert data["order_data"][0]["customer"] == order.user.email
        assert data["order_data"][0]["order_status"] == order.status

        # Verify product details in response
        products = data["order_data"][0]["products"]
        assert len(products) == 1
        assert products[0]["name"] == order_detail.product.name
        assert products[0]["quantity"] == order_detail.quantity
        assert float(products[0]["cost"]) == float(order_detail.cost)
        assert float(products[0]["total_cost"]) == float(order_detail.quantity * order_detail.cost)

    