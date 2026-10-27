from django.db import models
from django.contrib.auth.models import User

class UserAccountSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account_settings')
    email_notifications = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Settings for {self.user.username}"
