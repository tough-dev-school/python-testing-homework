import pytest


@pytest.fixture(autouse=True)
def seed(request):
    """Returns int for fake random seed for registration."""
    return request.config.getoption('randomly_seed')
