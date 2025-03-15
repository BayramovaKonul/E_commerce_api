import pytest
from rest_framework.exceptions import ValidationError
from products.models import CommentModel
from products.serializers import CommentRatingSerializer


@pytest.mark.django_db
class TestCommentRatingSerializer:
    def test_valid_comment(self):
        """Test the serializer with a valid comment and rating"""
        valid_data = {
            "comment": "This is a valid comment.",
        }

        serializer = CommentRatingSerializer(data=valid_data)

        assert serializer.is_valid()  
        assert serializer.validated_data["comment"] == "This is a valid comment."


    def test_missing_comment(self):
        """Test that the serializer raises an error if the comment field is missing"""
        invalid_data = {
            "comment": ""
        }

        serializer = CommentRatingSerializer(data=invalid_data)

        assert not serializer.is_valid()  
        assert "comment" in serializer.errors  


 


