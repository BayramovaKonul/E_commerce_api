from rest_framework import serializers
from ..models import CommentModel

class CommentRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ['comment', 'rating']

    def validate_rating(self, value):
        comment = self.initial_data.get('comment') 

        if comment and not value:
            raise serializers.ValidationError("You must provide a rating when writing a comment.")
        return value