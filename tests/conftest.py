import pytest
from django.test import RequestFactory, Client

from server.apps.identity.models import User

pytest_plugins = [
    # Should be the first custom one:
    'plugins.django_settings',
    'plugins.identity.user'
    # TODO: add your own plugins here!
]


@pytest.fixture(scope="session")
def request_factory():
    yield RequestFactory()


@pytest.fixture
def authorized_client(user: User, client: Client):
    client.force_login(user)
    yield client
