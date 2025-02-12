import pytest
from rest_framework.test import APIClient
from rest_framework import status
from account.models import ForgotPasswordTokenModel
from unittest.mock import patch
from ...confest import user, anonymous_client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

@pytest.mark.django_db

class TestForgotPasswordView:

    @patch("account.tasks.send_password_reset_email")
    def test_request_forgot_password_valid_email(self, mock_send_email, user, anonymous_client):
        """Test getting forgot-password email using a valid email address"""

        from django.utils.translation import activate
        activate('en')  # Ensures test runs in English without unwanted locale prefix

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
        
        # Verify that the password reset email was sent with the correct URL
        mock_send_email.assert_called_once_with(
            user.email,
            f"http://example.com/forgot-password?token={token.token}"
        )


    def test_request_forgot_password_invalid_email(self, anonymous_client):
        """Test not getting forgot-password email using  invalid email address"""
    
        url = reverse("forgot_password")
        data = {"email": "invaliduser@example.com"}
        
        response = anonymous_client.post(url, data, format="json")
        
        assert not response.status_code == status.HTTP_200_OK
        assert response.data["email"][0] == "No user found with this email address."

