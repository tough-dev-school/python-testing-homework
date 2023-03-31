import pytest
from django.test import Client

from server.apps.identity.models import User


@pytest.fixture()
def user_client(client: Client, user: User):
    client.force_login(user)
    return client
