"""
This module is used to provide configuration, fixtures, and plugins for pytest.

It may be also used for extending doctest's context:
1. https://docs.python.org/3/library/doctest.html
2. https://docs.pytest.org/en/latest/doctest.html
"""

import pytest
from django.test.client import Client
from mimesis import random

from server.apps.identity.models import User

pytest_plugins = [
    # Should be the first custom one:
    'tests.plugins.django_settings',
    'tests.plugins.identity.users',
    'tests.plugins.pictures.pictures',
]


@pytest.fixture()
def mimesis_seed() -> int:
    return random.Random().getrandbits(32)  # noqa: WPS432


@pytest.fixture()
def user_client(user: User) -> Client:
    client = Client()
    client.force_login(user)
    return client
