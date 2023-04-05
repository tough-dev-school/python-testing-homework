"""
This module is used to provide configuration, fixtures, and plugins for pytest.

It may be also used for extending doctest's context:
1. https://docs.python.org/3/library/doctest.html
2. https://docs.pytest.org/en/latest/doctest.html
"""
import random

import pytest

pytest_plugins = [
    "plugins.django_settings",
    "plugins.identity.user",
    "plugins.assertions.user",
    "plugins.pictures.pictures",
    "plugins.external_services.external",
]


@pytest.fixture(scope="session")
def faker_seed() -> int:
    return random.Random().getrandbits(32)
