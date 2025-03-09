import pytest
from rest_framework.exceptions import ValidationError
from products.models import CommentModel
from products.serializers import CommentRatingSerializer


@pytest.mark.django_db
class TestCommentRatingSerializer:
    def test_valid_comment_and_rating(self):
        """Test the serializer with a valid comment and rating"""
        valid_data = {
            "comment": "This is a valid comment.",
            "rating": 5
        }

        serializer = CommentRatingSerializer(data=valid_data)

        assert serializer.is_valid()  
        assert serializer.validated_data["comment"] == "This is a valid comment."
        assert serializer.validated_data["rating"] == 5


    def test_missing_rating_when_comment_exists(self):
        """Test that the serializer raises an error if a comment is provided but no rating"""
        invalid_data = {
            "comment": "This comment has no rating.",
            "rating": None
        }

        serializer = CommentRatingSerializer(data=invalid_data)

        assert not serializer.is_valid()  
        assert "rating" in serializer.errors  
        assert serializer.errors["rating"] == ["This field may not be null."]


    def test_missing_comment(self):
        """Test that the serializer raises an error if the comment field is missing"""
        invalid_data = {
            "comment": "",
            "rating": 4
        }

        serializer = CommentRatingSerializer(data=invalid_data)

        assert not serializer.is_valid()  
        assert "comment" in serializer.errors  


    def test_invalid_rating_below_min_value(self):
        """Test that the serializer raises an error if the rating is below 1"""
        invalid_data = {
            "comment": "This comment has an invalid rating.",
            "rating": 0
        }

        serializer = CommentRatingSerializer(data=invalid_data)

        assert not serializer.is_valid()  
        assert "rating" in serializer.errors 
        assert serializer.errors["rating"] == ["Ensure this value is greater than or equal to 1."]


    def test_invalid_rating_above_max_value(self):
        """Test that the serializer raises an error if the rating is above 5"""

        invalid_data = {
            "comment": "This comment has an invalid rating.",
            "rating": 6
        }

        serializer = CommentRatingSerializer(data=invalid_data)

        assert not serializer.is_valid()  
        assert "rating" in serializer.errors
        assert serializer.errors["rating"] == ["Ensure this value is less than or equal to 5."]


