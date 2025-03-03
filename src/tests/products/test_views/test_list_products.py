import pytest
from django.urls import reverse
from ...confest import anonymous_client, store, product, product2, category, user

@pytest.mark.django_db
class TestProductListView:

    def test_get_all_products(self, anonymous_client, product, product2):
        """Test retrieving all products"""

        url = reverse("all_products")  
        response = anonymous_client.get(url)
        
        assert response.status_code == 200
        assert response.data["count"] == 2 


    def test_search_product_by_name(self, anonymous_client, product, product2):
        """Test searching for a product by name"""

        url = reverse("all_products")  + "?search=Test Product 2"
        response = anonymous_client.get(url)

        assert response.status_code == 200
        assert response.data["count"] == 1
        assert response.data["results"][0]["name"] == "Test Product 2"


    def test_filter_products_by_latest(self, anonymous_client, product, product2):
        """Test filtering products by latest"""

        url = reverse("all_products")  + "?order=latest"
        response = anonymous_client.get(url)

        assert response.status_code == 200
        # list of products
        products = response.data["results"]
        assert len(products) == 2
        assert products[0]["name"] == "Test Product 2"  


    def test_filter_products_price_low_to_high(self, anonymous_client, product, product2):
        """Test filtering products from low to high price"""

        url = reverse("all_products")  + "?order=price_low_to_high"
        response = anonymous_client.get(url)

        assert response.status_code == 200
        products = response.data["results"]
        assert products[0]["price"] <= products[1]["price"]

