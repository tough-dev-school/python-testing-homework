"""
This module is used to provide configuration, fixtures, and plugins for pytest.

It may be also used for extending doctest's context:
1. https://docs.python.org/3/library/doctest.html
2. https://docs.pytest.org/en/latest/doctest.html
"""
import random

import pytest

pytest_plugins = [
    # Should be the first custom one:
    'plugins.django_settings',
    'plugins.identity.factories',
    'plugins.identity.asserts',
]

SEED_LENGTH = 32


@pytest.fixture()
def data_seed(faker_seed):
    """Default seed."""
    return faker_seed


@pytest.fixture(scope='session')
def update_data_seed():
    """Different seed for new data."""
    return random.Random().getrandbits(SEED_LENGTH)
