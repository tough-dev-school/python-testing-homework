import random

import pytest


@pytest.fixture(autouse=True)
def faker_seed():
    """Returns int for fake random seed for registration."""
    bits = 32
    return random.Random().getrandbits(bits)
