import pytest 
from django.urls import reverse
from rest_framework import status
from ...confest import (authenticated_client, user, anonymous_client, store, 
                        product_data_2, product, another_authenticated_client, category, another_user, image_file, product_data)
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
class TestUpdateProductView:

    # def test_update_product_with_valid_data(self, authenticated_client, product_data_2, product):
    #     """Test that user updates product with valid data """
    #     from django.utils.translation import activate
    #     activate('en')  # Ensures test runs in English without unwanted locale prefix

    #     url = reverse("update_product", args=[product.id])


    #     res = authenticated_client.patch(url, data=product_data_2, format='multipart')

    #     print(res.data)
    #     assert res.status_code == status.HTTP_200_OK
    #     assert res.data["message"] == "You updated your product details successfully"
    #     assert res.data["name"] == product_data_2["name"]
    #     assert res.data["description"] == product_data_2["description"]
    #     assert res.data["stock"] == product_data_2["stock"]


    def test_update_product_with_invalid_name(self, authenticated_client, product):
        """Test that user updates product with invalid name """

        url = reverse("update_product", args=[product.id])
        invalid_data = {"name": ""} 

        res = authenticated_client.patch(url, data=invalid_data, format='multipart')

        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert 'name' in res.data  


    def test_update_product_without_authentication(self, anonymous_client, product, product_data):
        """Test that user updates product without authentication """

        url = reverse("update_product", args=[product.id])


        res = anonymous_client.patch(url, data=product_data, format='multipart')

        assert res.status_code == status.HTTP_401_UNAUTHORIZED


    def test_update_product_not_owner(self, another_authenticated_client, product, product_data):
        """Test that a user who is not the owner cannot update the product"""

        url = reverse('update_product', kwargs={'product_id': product.id})
        
        response = another_authenticated_client.patch(url, data=product_data, format='multipart')
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == "You do not have permission to perform this action."

