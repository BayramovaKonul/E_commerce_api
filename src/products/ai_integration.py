import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def get_comment_rating(comment):
    # Send comment to OpenAI API
    prompt = f"""
    You are an analysis AI. Analyze the following user comment and give it a rating from 1 to 5, 
    where 1 is very negative, 3 is neutral, and 5 is very positive. 
    Provide only a single integer as the output.

    Comment: "{comment}"
    Rating:
    """

    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=[{"role": "user", "content": prompt}],
        max_tokens=60,
        temperature=0.5,  # controls the creativity or randomness - 0.5 = between predictability and creativity
    )
    
    # Extract and return the rating
    rating = response.choices[0].message.content.strip()

    try:
        rating = int(rating)  # Ensure it's an integer
        if rating < 1: rating = 1
        if rating > 5: rating = 5
    except ValueError:
        rating = 3  # Default rating if something goes wrong
    return rating
