from typing import Generator

import pytest

from server.apps.identity.models import User
from tests.plugins.identity.login import LoginData, LoginDataFactory
from tests.plugins.identity.registration import UserData


@pytest.fixture()
def login_data(
    login_data_factory: LoginDataFactory,
    user_data: UserData,
) -> LoginData:
    """Login data with all required fields."""
    return login_data_factory(username=user_data['email'])


@pytest.fixture()
def _mock_check_pwd(
    monkeypatch: pytest.MonkeyPatch,
) -> Generator[None, None, None]:
    """
    Mock password checking logic for the user.

    Always return True.
    """
    with monkeypatch.context() as mp:
        mp.setattr(target=User, name='check_password', value=lambda *args: True)
        yield
