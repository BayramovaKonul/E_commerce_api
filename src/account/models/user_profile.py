from django.db import models
from .custom_user import CustomUserModel
from django.contrib.auth import get_user_model

User= get_user_model()

class UserProfileModel(models.Model):
    birthday=models.DateField(null=True, blank=True)
    phone_number=models.CharField(null=True, blank=True)
    user=models.OneToOneField(CustomUserModel, on_delete=models.CASCADE,
                             related_name="profile")

    class Meta:
        db_table='user_profile'
        verbose_name='User_profile'
        verbose_name_plural='User_profiles'

    def __str__(self):
        return f"{self.user.first_name, self.user.last_name}"