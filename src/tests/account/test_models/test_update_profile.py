import pytest
from django.core.exceptions import ValidationError
from ...confest import user

@pytest.mark.django_db
def test_update_birthday_with_invalid_value(user):
    """Test that birthday cannot be updated with an invalid date."""
    
    # Invalid birthday 
    invalid_birthday = "invalid_date_string" 
    
    with pytest.raises(ValidationError, match=r"^.*invalid_date_string.*value has an invalid date format.*$"):
        user.profile.birthday = invalid_birthday
        user.profile.clean()  
        user.profile.save()  
