# tasks.py
from celery import shared_task
from .ai_integration import get_comment_rating
from .models import CommentModel  # Assuming you have a ProductReview model

@shared_task
def analyze_comment_and_rate(comment_id):
    review = CommentModel.objects.get(id=comment_id)
    comment = review.comment

    # Send the comment to OpenAI for analysis
    rating = get_comment_rating(comment)

    # Save the rating to the review
    review.rating = rating
    review.save()

    return f"Rating for comment {comment_id} is {rating}"
