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
    'plugins.identity.user',
]


def pytest_configure(config: pytest.Config) -> None:
    """
    Read randomly_seed from config.

    Set it from cache if present, set new if not and save to cache.
    """
    bits = 32
    seed_value = config.getoption('randomly_seed')
    default_seed = random.Random().getrandbits(bits)
    if seed_value == 'last':
        seed = config.cache.get(   # type: ignore[union-attr]
            'randomly_seed', default_seed,
        )
    elif seed_value == 'default':
        seed = default_seed
    else:
        seed = seed_value
    if hasattr(config, 'cache'):  # noqa: WPS421
        config.cache.set('randomly_seed', seed)  # type: ignore[union-attr]
    config.option.randomly_seed = seed
