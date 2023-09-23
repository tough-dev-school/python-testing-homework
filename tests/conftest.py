"""
This module is used to provide configuration, fixtures, and plugins for pytest.

It may be also used for extending doctest's context:
1. https://docs.python.org/3/library/doctest.html
2. https://docs.pytest.org/en/latest/doctest.html
"""

import pytest
import random


pytest_plugins = [
    # Should be the first custom one:
    'plugins.django_settings',
    'plugins.identity.user',
    'plugins.pictures.pictures'
    # TODO: add your own plugins here!
]


def pytest_configure(config: pytest.Config) -> None:
    seed_value = config.getoption("randomly_seed")
    # рандомный seed:
    default_seed = random.Random().getrandbits(32)

    if seed_value == 'last':
        seed = config.cache.get('randomly_seed', default_seed)
    elif seed_value == 'default':
        seed = default_seed
    else:
        seed = seed_value

    if hasattr(config, 'cache'):
        config.cache.set('randomly_seed', seed)
    config.option.randomly_seed = seed
