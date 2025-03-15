from rest_framework import serializers
from ..models import CommentModel
from e_commerce.models import OrderDetailsModel

class CommentRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ['comment']

