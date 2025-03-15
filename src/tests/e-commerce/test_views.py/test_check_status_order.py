import pytest
from django.urls import reverse
from rest_framework import status
from e_commerce.serializers import OrderDetailStatusSerializer
from tests.confest import order_detail, order, address, product, category, store, user, authenticated_client, another_user, another_authenticated_client


@pytest.mark.django_db
class TestOrderItemStatusView:
    def test_get_order_status(self, authenticated_client, order_detail):
        """Test retrieving order item status."""
        url = reverse("order_item_status", args=[order_detail.id]) 
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == OrderDetailStatusSerializer(order_detail).data


    def test_patch_order_status(self, authenticated_client, order_detail):
        """Test updating order item status."""
        url = reverse("order_item_status", args=[order_detail.id]) 
        new_status = {"status": "shipped"}  

        response = authenticated_client.patch(url, data=new_status, format="json")

        order_detail.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Order item status updated successfully"
        assert order_detail.status == "shipped"


    def test_unauthorized_access(self, another_authenticated_client, order_detail):
        """Test that unauthorized users cannot access the endpoint."""
        url = reverse("order_item_status", args=[order_detail.id])  
        response = another_authenticated_client.patch(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
