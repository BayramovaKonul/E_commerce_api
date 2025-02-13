import pytest
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from account.models import ForgotPasswordTokenModel
from ...confest import user


@pytest.mark.django_db
class TestForgotPasswordTokenModel:

    def test_token_creation(self, user):
        """Test that a ForgotPasswordTokenModel instance is created correctly when a user requests a password reset."""
        # Create a token for the user
        token = ForgotPasswordTokenModel.objects.create(user=user)

        # Assertions
        assert token.token is not None
        assert token.is_used is False
        assert token.expired_at > token.created_at
        assert token.user.email == user.email


    def test_token_expiration(self, user):
        """Test that the token expires after the specified time."""
        # Create a token for the user
        token = ForgotPasswordTokenModel.objects.create(user=user)

        # Initially, the token should not be expired
        assert token.is_expired() is False

        # Simulate expiration by setting the expired_at to a time in the past
        token.expired_at = timezone.now() - timedelta(seconds=1)
        token.save()

        # After saving, the token should be expired
        assert token.is_expired() is True


    def test_token_usage(self, user):
        """Test that a token is considered expired once it has been used."""
        # Create a token for the user
        token = ForgotPasswordTokenModel.objects.create(user=user)

        # Mark the token as used
        token.is_used = True
        token.save()

        # After saving, the token should be expired
        assert token.is_expired() is True


    def test_multiple_tokens(self, user):
        """Ensure multiple password reset requests create different tokens."""
        # Create two tokens for the same user
        token1 = ForgotPasswordTokenModel.objects.create(user=user)
        token2 = ForgotPasswordTokenModel.objects.create(user=user)

        # Assertions: Tokens should be unique
        assert token1.token != token2.token
