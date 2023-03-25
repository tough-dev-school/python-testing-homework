from typing import TYPE_CHECKING

import pytest
from django.test import Client
from mimesis.schema import Schema
from typing_extensions import Unpack

from server.apps.identity.models import User

if TYPE_CHECKING:
    from mimesis.schema import Field

    from tests.plugins.identity.user import (
        RegistrationData,
        RegistrationDataFactory,
        UserAssertion,
        UserData,
    )

_START_YEAR = 1900


@pytest.fixture()
def registration_data_factory(
    mimesis_field: 'Field',
) -> 'RegistrationDataFactory':
    """Returns factory for fake random registration data."""
    def factory(**fields: Unpack['RegistrationData']) -> 'RegistrationData':
        password = mimesis_field('password')  # by default passwords are equal
        schema = Schema(schema=lambda: {
            'email': mimesis_field('person.email'),
            'first_name': mimesis_field('person.first_name'),
            'last_name': mimesis_field('person.last_name'),
            'date_of_birth': mimesis_field(
                'datetime.date',
                start=_START_YEAR,
            ),
            'address': mimesis_field('address.city'),
            'job_title': mimesis_field('person.occupation'),
            'phone': mimesis_field('person.telephone'),
        })

        return {
            **schema.create(iterations=1)[0],  # type: ignore[misc]
            **{'password1': password, 'password2': password},
            **fields,
        }

    return factory


@pytest.fixture()
def registration_data(
    registration_data_factory: 'RegistrationDataFactory',
) -> 'RegistrationData':
    """Returns random registration data."""
    return registration_data_factory()


@pytest.fixture()
def expected_user_data(registration_data: 'RegistrationData') -> 'UserData':
    """We need to simplify registration data to drop password fields.

    Basically, it is the same as registration data, but without password fields.
    """
    return {  # type: ignore[return-value]
        key: value_part
        for key, value_part in registration_data.items()
        if not key.startswith('password')
    }


@pytest.fixture(scope='session')
def assert_correct_user() -> 'UserAssertion':
    """Returns assertion for user data."""
    def factory(email: str, expected: 'UserData') -> None:
        user = User.objects.get(email=email)

        # Special fields:
        assert user.id
        assert user.is_active
        assert not user.is_superuser
        assert not user.is_staff

        # All other fields:
        for field, data_value in expected.items():
            assert getattr(user, field) == data_value

    return factory


@pytest.fixture()
def logged_in_client(
    registration_data: 'RegistrationData',
    client: Client,
    django_user_model: User,
) -> Client:
    """Returns logged in client."""
    password = registration_data.pop('password1')
    registration_data.pop('password2')

    user = django_user_model.objects.create_user(
        **registration_data,
        password=password,
    )
    client.login(username=user.email, password=password)

    return client
