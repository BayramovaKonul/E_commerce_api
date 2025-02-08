import pytest
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db.utils import IntegrityError
import os
from django.core.files.uploadedfile import SimpleUploadedFile
from ...confest import user

@pytest.mark.django_db 
class TestCustomUserModel:

    @pytest.mark.django_db  
    def test_create_user(self, user):

        """Test that creating a new User and saving it to database"""

        assert user.email == "test@gmail.com"  
        assert user.first_name == "konul"
        assert user.last_name == "bayramova"
        assert user.is_staff == False
        assert user.is_superuser == False
        assert user.is_active == True


    @pytest.mark.django_db  # for connection with the database
    def test_create_super_user(self):

        """Test that creating Super User and saving to database"""
        email='test@gmail.com'
        first_name ='super'
        last_name = "user"
        password="123456"

        super_user=get_user_model().objects.create_superuser(
            email=email,
            first_name = first_name,
            last_name = last_name,
            password=password
        )

        assert super_user.email == email    # check if the created user's email is same with the email we sent
        assert super_user.first_name == first_name
        assert super_user.last_name == last_name
        assert super_user.check_password(password) == True
        assert super_user.is_staff == True
        assert super_user.is_superuser == True
        assert super_user.is_active == True


    @pytest.mark.django_db 
    def test_create_user_without_email(self):
        """"Test creating a new user without an email"""

        with pytest.raises(ValueError, match=str(_("The Email should be entered"))):
            get_user_model().objects.create_user(email = "", 
                                                 first_name = "check",
                                                 last_name = "user",
                                                 password = "1234"
                                                )
            
    @pytest.mark.django_db 
    def test_create_user_without_first_name(self):

        """"Test creating a new user without a first_name"""

        with pytest.raises(ValueError, match=str(_("The First name should be entered"))):
            get_user_model().objects.create_user(email="test3@gmail.com", 
                                                 first_name = "",
                                                 last_name = "user",
                                                 password="1234")
            
    @pytest.mark.django_db 
    def test_create_user_without_last_name(self):

        """"Test creating a new user without a first_name"""

        with pytest.raises(ValueError, match=str(_("The Last name should be entered"))):
            get_user_model().objects.create_user(email="test3@gmail.com", 
                                                 first_name = "check",
                                                 last_name = "",
                                                 password="1234")
            
    def test_unique_email(self):
        """Test creating a new user with a repeated email"""
        get_user_model().objects.create_user(email="test1@gmail.com", 
                                             first_name = "check",
                                             last_name = "user", 
                                             password='1234')
        
        with pytest.raises(IntegrityError):
            get_user_model().objects.create_user(email="test1@gmail.com", 
                                                 first_name = "check",
                                                 last_name = "user",
                                                 password='1234')
            


    def test_super_user_with_no_staff_status(self):
        """Test creating a super user with is_staff = False"""

        with pytest.raises(ValueError, match=str(_("Superuser must have is_staff=True."))):
            get_user_model().objects.create_superuser(email="test1@gmail.com", 
                                                      first_name = "super",
                                                      last_name = "user",
                                                      password='1234',
                                                      is_staff = False)
            
    def test_super_user_with_no_superuser_status(self):
        """Test creating a super user with is_superuser = False"""

        with pytest.raises(ValueError, match=str(_("Superuser must have is_superuser=True."))):
            get_user_model().objects.create_superuser(email="test1@gmail.com", 
                                                      first_name = "super",
                                                      last_name = "user",
                                                      password='1234',
                                                      is_superuser = False)


