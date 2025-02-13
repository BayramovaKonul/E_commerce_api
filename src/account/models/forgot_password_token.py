from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import uuid

User= get_user_model()

def get_expiry_date():
    expiration_duration = 1
    return timezone.now() + timedelta(days=expiration_duration)

class ForgotPasswordTokenModel(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="forgot_password_tokens", verbose_name=_("user"))
    
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(default=get_expiry_date)
    
    class Meta:
        db_table='forgot_password_token'
        verbose_name=_('Forgot_password_token')
        verbose_name_plural=_('Forgot_password_tokens')

    def __str__(self):
        return f"{self.user.first_name} -> {self.created_at}"
    

    def is_expired(self):
        return self.is_used or timezone.now() > self.expired_at
