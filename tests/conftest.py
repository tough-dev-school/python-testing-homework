"""
This module is used to provide configuration, fixtures, and plugins for pytest.

It may be also used for extending doctest's context:
1. https://docs.python.org/3/library/doctest.html
2. https://docs.pytest.org/en/latest/doctest.html
"""

import pytest
from django.test.client import Client

from server.apps.identity.models import User
from mimesis import random


pytest_plugins = [
    # Should be the first custom one:
    'plugins.django_settings',
    'plugins.identity.users',
    'plugins.pictures.pictures',
]


@pytest.fixture()
def mimesis_seed() -> int:
    return random.Random().getrandbits(32)


@pytest.fixture()
def user_client(user: User) -> Client:
    client = Client()
    client.force_login(user)
    return client
