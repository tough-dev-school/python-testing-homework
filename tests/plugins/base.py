import random

import pytest
from mimesis.locales import Locale
from mimesis.schema import Field

_RANDOM_BITS = 32


@pytest.fixture(scope='session')
def faker_seed() -> int:
    """Returns random seed for faker."""
    return random.Random().getrandbits(_RANDOM_BITS)


@pytest.fixture(scope='session')
def mimesis_field(faker_seed: int) -> Field:
    """Returns mimesis field with random seed."""
    return Field(locale=Locale.RU, seed=faker_seed)
