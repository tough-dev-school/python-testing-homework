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
    "plugins.django_settings",
    # TODO: add your own plugins here!
    "plugins.identity.user",
]


@pytest.fixture(scope="session")
def faker_seed() -> int:
    """Generates random seed for a fake data"""
    return random.Random().getrandbits(32)
