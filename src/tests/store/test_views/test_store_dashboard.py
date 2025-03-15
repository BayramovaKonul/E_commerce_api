import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from tests.confest import user, authenticated_client, product, address, store, category, order, order_detail, add_comments, another_user, another_authenticated_client, product2
from django.urls import reverse

@pytest.mark.django_db
class TestStoreDashboardView:
    
    def test_store_dashboard_access_for_non_owner(self, another_authenticated_client, store):
        """Test that a user who is not the owner cannot view the store dashboard"""

        url = reverse("store_dashboard", args=[store.id])

        response = another_authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error'] == "You are not allowed to view the store dashboard. You are not the owner."


    def test_store_not_found(self, store, authenticated_client):
        """Test that an owner cannot view store dashboard when a store is not found"""

        url = reverse("store_dashboard", args=(9999,))

        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['error'] == "Store not found"


    def test_successful_dashboard_data(self, authenticated_client, store, order, order_detail, product, product2, add_comments):
        """Test that a user who is the owner can view the store dashboard"""

        url = reverse("store_dashboard", args=[store.id])

        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'total_products' in response.data
        assert 'total_customers' in response.data
        assert 'total_profit' in response.data
        assert 'total_comments' in response.data
        assert 'total_sold_products' in response.data
        assert 'store_rating' in response.data
        assert 'order_data' in response.data
        

        assert response.data['total_products'] == 2 
        assert response.data['total_customers'] == 1 
        assert float(response.data['total_profit']) == 5.99  
        assert response.data['total_comments'] == 3 
        assert response.data['total_sold_products'] == 1
        assert float(response.data['store_rating']) == 4.0  

