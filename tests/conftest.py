"""
This module is used to provide configuration, fixtures, and plugins for pytest.

It may be also used for extending doctest's context:
1. https://docs.python.org/3/library/doctest.html
2. https://docs.pytest.org/en/latest/doctest.html
"""

import pytest
from server.apps.identity.models import User

pytest_plugins = [
    # Should be the first custom one:
    'plugins.django_settings',
    'plugins.identity.pytest_identity',
    'plugins.pictures.pytest_pictures',
]


@pytest.fixture
# @pytest.mark.django_db
def user() -> None:
    user = User(email='aa')
    user.save()
    yield user
    user.delete()
