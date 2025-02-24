import pytest
import uuid
from django.utils.timezone import now
from django.urls import reverse
from rest_framework import status
from ...confest import user, anonymous_client, validation_token

@pytest.mark.django_db
class TestValidateEmailView:

    def test_validate_email_with_valid_token(self, anonymous_client, user, validation_token):
        url = reverse('validate_email')  
        response = anonymous_client.post(url, {'token': validation_token.token}, format='json')

        validation_token.refresh_from_db()
        user.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == "Email validated successfully!"

        assert validation_token.is_used is True
        assert validation_token.expired_at is not None
        # check token is expired after validation
        assert abs((validation_token.expired_at - now()).total_seconds()) < 5

        assert user.is_active is True


    def test_validate_email_invalid_token(self, anonymous_client):

        url = reverse('validate_email') 
        response = anonymous_client.post(url, {'token': str(uuid.uuid4())}, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
