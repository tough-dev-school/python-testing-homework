from datetime import date

import pytest
from django.test import Client


@pytest.fixture()
def admin_client_app(django_user_model, django_username_field: str):
    """Make admin user client."""
    username_field = django_username_field
    username = 'admin@example.com' if username_field == 'email' else 'admin'

    try:
        user = django_user_model._default_manager.get_by_natural_key(username)
    except django_user_model.DoesNotExist:
        user_data = {}
        if 'email' in django_user_model.REQUIRED_FIELDS:
            user_data['email'] = 'admin@example.com'
        user_data['password'] = 'password'
        user_data['date_of_birth'] = str(date.today())
        user_data[username_field] = username
        user = django_user_model._default_manager.create_superuser(**user_data)

    client = Client()
    client.force_login(user)
    return client
