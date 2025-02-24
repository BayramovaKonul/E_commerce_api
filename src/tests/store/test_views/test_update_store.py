import pytest 
from django.urls import reverse
from rest_framework import status
from ...confest import authenticated_client, user, store_data, anonymous_client, store
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
class TestUpdateStoreView:

    def test_update_store_with_valid_data(self, authenticated_client, store_data, store):
        """Test that user updates store with valid credentials """
        from django.utils.translation import activate
        activate('en')  # Ensures test runs in English without unwanted locale prefix

        url = reverse("update_store", args=[store.id])


        res = authenticated_client.patch(url, data=store_data, format='multipart')

        assert res.status_code == status.HTTP_200_OK
        assert res.data["message"] == "You updated your store details successfully"
        assert res.data["name"] == store_data["name"]
        assert res.data["description"] == store_data["description"]
        assert res.data["address"] == store_data["address"]


    def test_update_store_with_invalid_name(self, authenticated_client, store_data, store):
        """Test that user updates store with invalid name """

        url = reverse("update_store", args=[store.id])
        invalid_data = {"name": ""}  # Invalid data

        res = authenticated_client.patch(url, data=invalid_data, format='multipart')

        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert 'name' in res.data 


    def test_update_store_without_authentication(self, anonymous_client, store_data, store):
        """Test that user updates store without authentication """

        url = reverse("update_store", args=[store.id])


        res = anonymous_client.patch(url, data=store_data, format='multipart')

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

