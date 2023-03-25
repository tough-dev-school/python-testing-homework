"""
This module is used to provide configuration, fixtures, and plugins for pytest.

It may be also used for extending doctest's context:
1. https://docs.python.org/3/library/doctest.html
2. https://docs.pytest.org/en/latest/doctest.html
"""

import pytest

from server.apps.pictures.container import container
from server.common.django.types import Settings

pytest_plugins = [
    'plugins.django_settings',
    'plugins.mimesis_fake',
    'plugins.identity.pytest_identity',
    'plugins.pictures.pytest_pictures',
]


@pytest.fixture()
def settings() -> Settings:
    """Get Django settings."""
    return container.resolve(Settings)
