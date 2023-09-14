from server.apps.identity.models import User
from mixer.backend.django import mixer

import pytest


@pytest.fixture
def user() -> User:
    user = mixer.blend(User)
    yield user
    user.delete()
