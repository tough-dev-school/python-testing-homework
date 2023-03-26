from datetime import datetime
from typing import Protocol, TypedDict, Union

import pytest
from mimesis.schema import Field, Schema
from typing_extensions import Unpack


class UserUpdateData(TypedDict, total=False):
    """User data that is required to update an existing user."""

    first_name: str
    last_name: str
    date_of_birth: Union[datetime, str]
    address: str
    job_title: str
    phone: str


class UserUpdateDataFactory(Protocol):
    """User update data factory protocol."""

    def __call__(
        self,
        **fields: Unpack[UserUpdateData],
    ) -> UserUpdateData:
        """Return user update data on call."""


@pytest.fixture()
def user_update_data_factory(
    fake_field: Field,
) -> UserUpdateDataFactory:
    """Factory for fake random data for user update."""

    def factory(**fields: Unpack[UserUpdateData]) -> UserUpdateData:
        schema = Schema(
            schema=lambda: {
                'first_name': fake_field('person.first_name'),
                'last_name': fake_field('person.last_name'),
                'date_of_birth': fake_field('datetime.date'),
                'address': fake_field('address.city'),
                'job_title': fake_field('person.occupation'),
                'phone': fake_field('person.telephone'),
            },
        )
        return {
            **schema.create(iterations=1)[0],  # type: ignore[misc]
            **fields,
        }

    return factory
