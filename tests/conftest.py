"""
This module is used to provide configuration, fixtures, and plugins for pytest.

It may be also used for extending doctest's context:
1. https://docs.python.org/3/library/doctest.html
2. https://docs.pytest.org/en/latest/doctest.html
"""

import random

import pytest
from mimesis.locales import Locale
from mimesis.schema import Field

pytest_plugins = [
    # Should be the first custom one:
    'tests.plugins.django_settings',
    'tests.plugins.identity.login',
    'tests.plugins.identity.registration',
    'tests.plugins.identity.user_update',
    'tests.plugins.pictures.picture',
]


RANDOM_SEED_LENGTH = 32


@pytest.fixture(scope='session', autouse=True)
def faker_seed() -> int:
    """Fake seed for random data generation."""
    return random.Random().getrandbits(RANDOM_SEED_LENGTH)


@pytest.fixture()
def fake_field(faker_seed: int) -> Field:
    """Fake mimesis field for custom data types."""
    return Field(locale=Locale.RU, seed=faker_seed)
