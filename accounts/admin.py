from django.contrib import admin
from .models import UserAccountSetting

@admin.register(UserAccountSetting)
class UserAccountSettingAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_notifications', 'created_at', 'updated_at')
