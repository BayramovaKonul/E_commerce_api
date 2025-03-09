import uuid
from .models import ValidateUserTokenModel
from django.urls import reverse
from django.conf import settings

def generate_token(user):
    token = str(uuid.uuid4())  # Generating a unique token using uuid
    validation_token = ValidateUserTokenModel(user=user, token=token)
    validation_token.save()
    return token


def generate_validation_link(user, token):

    validation_url = reverse('validate_email')  
    domain = settings.VALIDATE_USER_URL  

    validation_link = f"{domain}{validation_url}?token={token}"
    
    return validation_link

