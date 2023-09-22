"""
This module is used to provide configuration, fixtures, and plugins for pytest.

It may be also used for extending doctest's context:
1. https://docs.python.org/3/library/doctest.html
2. https://docs.pytest.org/en/latest/doctest.html
"""
import pytest

pytest_plugins = [
    # Should be the first custom one:
    'plugins.django_settings',

    # TODO: add your own plugins here!
]


@pytest.fixture()
def mixer():
    """Util for create models."""
    from mixer.backend.django import mixer  # noqa: WPS433 names conflict
    return mixer


@pytest.fixture()
def exists_user(mixer):
    """User registered in system."""
    return mixer.blend('identity.User')


@pytest.fixture()
def user_client(exists_user, client):
    """Registered user HTTP client."""
    client.force_login(exists_user)
    return client
