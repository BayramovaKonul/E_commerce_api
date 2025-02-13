import pytest
from rest_framework.test import APIClient
from rest_framework import status
from account.models import ForgotPasswordTokenModel
from unittest.mock import patch
from ...confest import user, anonymous_client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings
from django.core import mail

@pytest.mark.django_db

class TestForgotPasswordView:

    def test_request_forgot_password_valid_email(self, user, anonymous_client):
        """Test getting forgot-password email using a valid email address"""

        # Set the language to English for the test
        from django.utils.translation import activate
        activate('en')

        url = reverse("forgot_password")
        data = {'email': user.email}

        response = anonymous_client.post(url, data, format="json")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Password reset email sent."
        assert "token" in response.data
        
        # Check if a reset token was created for the user
        token = ForgotPasswordTokenModel.objects.filter(user=user).first()
        assert token is not None
        assert not token.is_used
        
        # Assert that an email was sent
        assert len(mail.outbox) == 1  # Ensure exactly one email was sent
        email = mail.outbox[0]
        
        # Verify the email details (subject, recipient, and body)
        assert email.subject == "Password Reset Request"
        assert email.to == [user.email]
        assert f"{settings.RESET_PASSWORD_URL}?token={token.token}" in email.body


    def test_request_forgot_password_invalid_email(self, anonymous_client):
        """Test not getting forgot-password email using  invalid email address"""
    
        url = reverse("forgot_password")
        data = {"email": "invaliduser@example.com"}
        
        response = anonymous_client.post(url, data, format="json")
        
        assert not response.status_code == status.HTTP_200_OK
        assert response.data["email"][0] == "No user found with this email address."

