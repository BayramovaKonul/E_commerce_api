import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from ...confest import authenticated_client, product, store, category, user
from products.models import CommentModel

@pytest.mark.django_db
class TestCommentProductView:

    def test_post_comment_with_valid_data(self, authenticated_client, product, user):
        """Test successful comment posting"""

        valid_comment_data = {
            'comment': 'Great product!',
            'rating': 5
        }

        url = reverse('rate_product', args=[product.id]) 
        response = authenticated_client.post(url, data=valid_comment_data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['message'] == "Thanks for your comment"
        assert response.data['comment'] == valid_comment_data['comment']
        assert response.data['rating'] == valid_comment_data['rating']

        # check that the comment has been saved to the database
        comment = CommentModel.objects.get(product=product)
        assert comment.comment == valid_comment_data['comment']
        assert comment.rating == valid_comment_data['rating']
        assert comment.user == user


    def test_post_comment_missing_rating(self, authenticated_client, product):
        """Test posting comment with missing rating"""
        invalid_comment_data = {
            'comment': 'Good product!',
        }

        url = reverse('rate_product', args=[product.id])  
        response = authenticated_client.post(url, data=invalid_comment_data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "rating" in response.data
        assert response.data["rating"] == ["This field is required."]


    def test_post_comment_without_comment_field(self, authenticated_client, product):
        """Test posting comment with no comment field"""
        invalid_data = {'rating': 3}

        url = reverse('rate_product', args=[product.id]) 
        response = authenticated_client.post(url, data=invalid_data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "comment" in response.data
        assert response.data["comment"] == ["This field is required."]
