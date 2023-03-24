from typing import TYPE_CHECKING, Generator, Protocol, TypedDict, final

import pytest
from mimesis.locales import Locale
from mimesis.schema import Field, Schema
from typing_extensions import Unpack

from server.apps.identity.models import User

if TYPE_CHECKING:
    from plugins.identity.user import UserData


@final
class LoginData(TypedDict, total=False):
    """Represent the login data that is required to sign in user.

    Importing this type is only allowed under ``if TYPE_CHECKING`` in tests.
    """

    username: str
    password: str


@final
class LoginDataFactory(Protocol):
    """Login data factory protocol."""

    def __call__(self, **fields: Unpack[LoginData]) -> LoginData:
        """User login data factory protocol."""


@pytest.fixture()
def login_data_factory(faker_seed: int) -> LoginDataFactory:
    """Factory for fake random login data."""

    def factory(**fields: Unpack[LoginData]) -> LoginData:
        mf = Field(locale=Locale.RU, seed=faker_seed)
        schema = Schema(
            schema=lambda: {
                'username': mf('person.email'),
                'password': mf('password'),
            },
        )
        return {
            **schema.create(iterations=1)[0],  # type: ignore[misc]
            **fields,
        }

    return factory


@pytest.fixture()
def login_data(
    login_data_factory: LoginDataFactory,
    user_data: 'UserData',
) -> LoginData:
    """Returns random login data with all required fields for user sign in."""
    return login_data_factory(username=user_data['email'])


@pytest.fixture()
def _mock_check_pass(
    monkeypatch: pytest.MonkeyPatch,
) -> Generator[None, None, None]:
    """Mock password checking logic for the user. Always return True."""
    with monkeypatch.context() as mp:
        mp.setattr(target=User, name='check_password', value=lambda *args: True)
        yield
