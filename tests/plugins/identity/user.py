from server.apps.identity.models import User
from mixer.backend.django import mixer

import pytest


@pytest.fixture
def user() -> User:
    user = mixer.blend(User, date_of_birth=mixer.RANDOM)
    yield user
    user.delete()
