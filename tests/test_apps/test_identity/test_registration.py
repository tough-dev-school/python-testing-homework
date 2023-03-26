import random
from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from mimesis.locales import Locale
from mimesis.schema import Field, Schema
from typing_extensions import Unpack

if TYPE_CHECKING:

    from tests.plugins.identity.user import (
        RegistrationData,
        RegistrationDataFactory,
        UserAssertion,
        UserData,
    )


@pytest.fixture()
def faker_seed():
    """Returns int for fake random seed for registration."""
    bits = 32
    return random.Random().getrandbits(bits)


@pytest.fixture()
def registration_data_factory(
    faker_seed: int,
) -> 'RegistrationDataFactory':
    """Returns factory for fake random data for registration."""

    def factory(**fields: Unpack['RegistrationData']) -> 'RegistrationData':
        mf = Field(locale=Locale.RU, seed=faker_seed)
        password = mf('password')  # by default passwords are equal
        schema = Schema(schema=lambda: {
            'email': mf('person.email'),
            'first_name': mf('person.first_name'),
            'last_name': mf('person.last_name'),
            'date_of_birth': mf('datetime.date'),
            'address': mf('address.city'),
            'job_title': mf('person.occupation'),
            'phone': mf('person.telephone'),
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
    """Default success registration data."""
    return registration_data_factory()


@pytest.fixture(scope='session')
def assert_correct_user() -> 'UserAssertion':
    """Assert user data."""
    def factory(email: str, expected: 'UserData') -> None:
        user_model = get_user_model()
        user = user_model.objects.get(email=email)
        # Special fields:
        assert user.id
        assert user.is_active
        assert not user.is_superuser
        assert not user.is_staff
        # All other fields:
        for field_name, data_value in expected.items():
            assert getattr(user, field_name) == data_value

    return factory


@pytest.fixture()
def expected_user_data(registration_data: 'RegistrationData') -> 'UserData':
    """
    We need to simplify registration data to drop passwords.

    Basically, it is the same as ``registration_data``, but without passwords.
    """
    return {  # type: ignore[return-value]
        key_name: value_part
        for key_name, value_part in registration_data.items()
        if not key_name.startswith('password')
    }


@pytest.mark.django_db()
def test_valid_registration(
    client: Client,
    registration_data: 'RegistrationData',
    expected_user_data: 'UserData',
    assert_correct_user: 'UserAssertion',
) -> None:
    """Test that registration works with correct user data."""
    response = client.post(
        reverse('identity:registration'),
        data=registration_data,
    )
    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location') == reverse('identity:login')
    assert_correct_user(registration_data['email'], expected_user_data)
