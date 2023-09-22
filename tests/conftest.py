import pytest
from django.test import RequestFactory, Client

from server.apps.identity.models import User

pytest_plugins = [
    # Should be the first custom one:
    'plugins.django_settings',
    'plugins.identity.user'
]


@pytest.fixture(scope="session")
def request_factory():
    yield RequestFactory()


@pytest.fixture
def authorized_client(user: User, client: Client):
    client.force_login(user)
    yield client


@pytest.fixture()
def json_server_on(settings):
    previous_setting = settings.PLACEHOLDER_API_URL
    settings.PLACEHOLDER_API_URL = "http://json_server:5200/"
    yield
    settings.PLACEHOLDER_API_URL = previous_setting
