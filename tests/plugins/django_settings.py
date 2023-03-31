import pytest
from django.core.cache import BaseCache, caches


@pytest.fixture(autouse=True)
def _media_root(settings, tmpdir_factory) -> None:
    """Forces django to save media files into temp folder."""
    settings.MEDIA_ROOT = tmpdir_factory.mktemp('media', numbered=True)


@pytest.fixture(autouse=True)
def _password_hashers(settings) -> None:
    """Forces django to use fast password hashers for tests."""
    settings.PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]


@pytest.fixture(autouse=True)
def _auth_backends(settings) -> None:
    """Deactivates security backend from Axes app."""
    settings.AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
    )


@pytest.fixture(autouse=True)
def _debug(settings) -> None:
    """Sets proper DEBUG and TEMPLATE debug mode for coverage."""
    settings.DEBUG = False
    for template in settings.TEMPLATES:
        template['OPTIONS']['debug'] = True


@pytest.fixture(autouse=True)
def cache(settings) -> BaseCache:
    """Modifies how cache is used in Django tests."""
    test_cache = 'test'

    # Patching cache settings:
    settings.CACHES[test_cache] = {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
    settings.RATELIMIT_USE_CACHE = test_cache
    settings.AXES_CACHE = test_cache

    # Clearing cache:
    caches[test_cache].clear()
    return caches[test_cache]


@pytest.fixture(autouse=True)
def _debug(settings) -> None:
    """Sets proper DEBUG and TEMPLATE debug mode for coverage."""
    settings.DEBUG = True
    for template in settings.TEMPLATES:
        template['OPTIONS']['debug'] = True
