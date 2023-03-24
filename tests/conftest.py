"""
This module is used to provide configuration, fixtures, and plugins for pytest.

It may be also used for extending doctest's context:
1. https://docs.python.org/3/library/doctest.html
2. https://docs.pytest.org/en/latest/doctest.html
"""
import os
import random
from typing import Callable, List
from urllib.parse import urljoin

import pytest

pytest_plugins = [
    # Should be the first custom one:
    'plugins.django_settings',

    'plugins.identity.user',
    'plugins.identity.registration',
    'plugins.identity.login',

    'plugins.pictures.picture',
]


def pytest_configure(config: pytest.Config) -> None:
    """Read randomly seed from pytest config.

    Set it from cache if existed, set new if not and save to cache.
    """
    seed_length_in_bits = 32
    seed_value = config.getoption('randomly_seed')
    # random seed:
    default_seed = random.Random().getrandbits(seed_length_in_bits)

    if seed_value == 'last':
        seed = config.cache.get('randomly_seed', default_seed)
    elif seed_value == 'default':
        seed = default_seed
    else:
        seed = seed_value

    # saving to cache
    cache = getattr(config, 'cache', None)
    if cache is not None:
        config.cache.set('randomly_seed', seed)
    config.option.randomly_seed = seed


def pytest_collection_modifyitems(
    items: List[pytest.Item],  # noqa: WPS110
) -> None:
    """Add timeout mark for slow tests."""
    conn_timeout_in_sec = 2
    for item in items:  # noqa: WPS110
        if 'registration' in item.nodeid:
            item.add_marker(pytest.mark.registration)
        elif 'login' in item.nodeid:
            item.add_marker(pytest.mark.login)
        for _ in item.iter_markers(name='slow'):
            item.add_marker(pytest.mark.timeout(conn_timeout_in_sec))


@pytest.fixture(scope='session', autouse=True)
def faker_seed(request) -> int:
    """Generating a random sequence of numbers."""
    return request.config.getoption('randomly_seed')


@pytest.fixture(scope='session')
def external_api_url_factory() -> Callable[[str], str]:
    """Returns factory to build the full path to the json server."""
    def factory(path: str) -> str:
        return urljoin(os.getenv('JSON_SERVER_SERVICE'), path)

    return factory
