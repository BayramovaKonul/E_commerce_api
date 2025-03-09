import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from products.models import CommentModel
from ...confest import user, product, store, category


@pytest.mark.django_db
class TestCommentModel:
    def test_create_valid_comment(self, user, product):
        """Test creating a valid comment"""
        comment_data = {
            "comment": "This is a valid comment.",
            "rating": 5,
            "user": user,
            "product": product
        }

        comment = CommentModel.objects.create(**comment_data)

        assert comment.comment == "This is a valid comment."
        assert comment.rating == 5
        assert comment.user == user
        assert comment.product == product
  

    def test_comment_missing_rating(self, user, product):
        """Test that an exception is raised when a comment has no rating"""
        with pytest.raises(IntegrityError):
            CommentModel.objects.create(
                comment="This comment is missing a rating.",
                rating=None,  
                user=user,
                product=product
            )


    def test_comment_invalid_rating(self, user, product):
        """Test that an exception is raised when rating is out of 1-5 interval"""

        comment = CommentModel(comment="This comment has an invalid rating.", 
                               rating=10, 
                               user=user, 
                               product=product)
        
        with pytest.raises(ValidationError):
            comment.full_clean()


    def test_comment_without_comment_field(self, user, product):
        """Test that an exception is raised if the comment field is empty"""
        comment = CommentModel(comment="", 
                               rating=5, 
                               user=user, 
                               product=product)
        
        with pytest.raises(ValidationError):
            comment.full_clean()


    def test_comment_creation_user_not_authenticated(self, product):
        """Test that a comment cannot be created if the user is not authenticated"""
        with pytest.raises(IntegrityError): 
            CommentModel.objects.create(
                comment="This comment has no user.",
                rating=3,
                user=None,  
                product=product
            )


    def test_string_representation(self, user, product):
        """Test the string representation of a comment"""
        comment = CommentModel.objects.create(
            comment="Great product!",
            rating=4,
            user=user,
            product=product
        )
        assert str(comment) == "Great product! -> 4"
