from django.contrib.auth.views import LogoutView
from django.urls import path

from server.apps.identity.views.login import LoginView, RegistrationView
from server.apps.identity.views.user import UserUpdateView

app_name = 'identity'

urlpatterns = [
    # Login mechanics:
    path(
        'login',
        LoginView.as_view(template_name='identity/pages/login.html'),
        name='login',
    ),
    path('logout', LogoutView.as_view(), name='logout'),
    path('registration', RegistrationView.as_view(), name='registration'),

    # User updating:
    path('update', UserUpdateView.as_view(), name='user_update'),
]
