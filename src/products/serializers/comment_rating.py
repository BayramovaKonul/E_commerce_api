from rest_framework import serializers
from ..models import CommentModel

class CommentRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ['comment']

