# Django
from django.urls import path

# Project
from apps.gauth.views import AuthUserView, MeUserView, ChangePasswordView

app_name = 'apps.gauth'

urlpatterns = [
    path('auth/', AuthUserView.as_view(), name='auth'),
    path('me/', MeUserView.as_view(), name='me'),
    path('me/change-password',
         ChangePasswordView.as_view(), name='change-password'),
]
