import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from ...confest import authenticated_client, product, store, category, user, order, order_detail, address
from products.models import CommentModel
from unittest.mock import patch
from products.tasks import analyze_comment_and_rate

@pytest.mark.django_db
class TestCommentProductView:

    def test_post_comment_with_valid_data(self, authenticated_client, product, user, order, order_detail):
        """Test successful comment posting"""

        valid_comment_data = {
            'comment': 'Great product!',
        }

        assert order.user == user
        assert order_detail.product == product
        assert order_detail.order == order

        url = reverse('rate_product', args=[product.id]) 
        response = authenticated_client.post(url, data=valid_comment_data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['message'] == "Thanks for your comment"
        assert response.data['comment'] == valid_comment_data['comment']

        # check that the comment has been saved to the database
        comment = CommentModel.objects.get(product=product)
        assert comment.comment == valid_comment_data['comment']
        assert comment.user == user


    def test_post_comment_without_comment_field(self, authenticated_client, product):
        """Test posting comment with no comment field"""
        invalid_data = {'rating': 3}

        url = reverse('rate_product', args=[product.id]) 
        response = authenticated_client.post(url, data=invalid_data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "comment" in response.data
        assert response.data["comment"] == ["This field is required."]


    @patch("products.views.comment_rating.analyze_comment_and_rate.delay")  # Mock Celery task
    def test_post_comment(self, mock_celery_task, authenticated_client, product, order, order_detail, user):

        data = {"comment": "Great product!"}

        url = reverse('rate_product', args=[product.id])
        response = authenticated_client.post(url, data=data, format='json')

        assert order.user == user
        assert order_detail.product == product
        assert order_detail.order == order

        assert response.status_code == 201
        assert CommentModel.objects.count() == 1  
        assert mock_celery_task.called  


    @patch("products.tasks.get_comment_rating", return_value=5)  # Mock OpenAI API
    def test_analyze_comment_task(self, mock_rating, product, user):
        comment = CommentModel.objects.create(product=product, user=user, comment="Amazing!")
        analyze_comment_and_rate(comment.id)

        comment.refresh_from_db()
        assert comment.rating == 5  
        mock_rating.assert_called_once_with("Amazing!")  # to ensure OpenAI was called
