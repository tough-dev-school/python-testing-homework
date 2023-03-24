"""
This module is used to provide configuration, fixtures, and plugins for pytest.

It may be also used for extending doctest's context:
1. https://docs.python.org/3/library/doctest.html
2. https://docs.pytest.org/en/latest/doctest.html
"""
import random
from typing import Final

import pytest

pytest_plugins = [
    # Should be the first custom one:
    'plugins.django_settings',

    'plugins.identity.user',
    'plugins.identity.registration',
    'plugins.identity.login',

    'plugins.pictures.picture',
]

_SEED_LENGTH_IN_BITS: Final = 32


@pytest.fixture(scope='session', autouse=True)
def faker_seed() -> int:
    """Generating a random sequence of numbers."""
    return random.Random().getrandbits(_SEED_LENGTH_IN_BITS)
