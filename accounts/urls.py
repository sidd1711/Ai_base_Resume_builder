from django.urls import path
from .views import (
    RegisterView, LoginUserView, LogoutUserView,
    AccountSettingsView, DeleteAccountView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('settings/', AccountSettingsView.as_view(), name='account_settings'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete_account'),
]
