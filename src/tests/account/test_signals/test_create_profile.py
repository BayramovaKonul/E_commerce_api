import pytest
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db.utils import IntegrityError
from account.models import UserProfileModel
from ...confest import user

@pytest.mark.django_db 

def test_create_user_profile_using_signal(user):
    """Test that creating a user profile automatically after user registers"""

    # since we already have User fixture, no need to create a new user here
    profile=UserProfileModel.objects.get(user=user)

    assert profile.user == user  # Ensure the profile is linked to the correct user
    assert profile.user.email == user.email  
    assert profile.user.first_name == user.first_name  
    assert profile.user.last_name == user.last_name  