from typing import Protocol, TypedDict

import pytest
from mimesis.schema import Field, Schema
from typing_extensions import Unpack


class LoginData(TypedDict, total=False):
    """User data that is required to login to the app."""

    username: str
    password: str


class LoginDataFactory(Protocol):
    """Login data factory protocol."""

    def __call__(self, **fields: Unpack[LoginData]) -> LoginData:
        """Return login data on call."""


@pytest.fixture()
def login_data_factory(fake_field: Field) -> LoginDataFactory:
    """Factory for fake random data for login."""

    def factory(**fields: Unpack[LoginData]) -> LoginData:
        schema = Schema(
            schema=lambda: {
                'username': fake_field('person.email'),
                'password': fake_field('password'),
            },
        )
        return {
            **schema.create(iterations=1)[0],  # type: ignore[misc]
            **fields,
        }

    return factory
