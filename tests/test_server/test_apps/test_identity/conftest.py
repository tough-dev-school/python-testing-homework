from typing import Any, Unpack

import pytest
from mimesis import Field, Schema
from mimesis.locales import Locale

from server.apps.identity.models import User
from tests.plugins.identity.user import RegistrationDataFactory, RegistrationData, UserAssertion, UserData


@pytest.fixture()
def registration_data_factory() -> RegistrationDataFactory:
    def factory(**fields: Unpack[RegistrationData]) -> RegistrationData:
        field = Field(locale=Locale.RU, seed=fields.pop('seed'))
        password = field('password')
        schema = Schema(schema=lambda: {
            'email': field('person.email'),
            'first_name': field('person.first_name'),
            'last_name': field('person.last_name'),
            'date_of_birth': field('datetime.date'),
            'address': field('address.city'),
            'job_title': field('person.occupation'),
            'phone': field('person.telephone'),
        })
        return {
            **schema.create()[0],
            **{'password_first': password, 'password_second': password},
            **fields,
        }

    return factory


@pytest.fixture(scope='session')
def assert_correct_user() -> UserAssertion:
    def factory(email: str, expected: UserData) -> None:
        user = User.objects.get(email=email)
        assert user.id
        assert user.is_active
        assert not user.is_superuser
        assert not user.is_staff
        for field, value in expected.items():
            assert getattr(user, field) == value

    return factory


@pytest.fixture()
def reg_data(registration_data_factory) -> RegistrationData:
    yield registration_data_factory(seed=1)


@pytest.fixture()
def expected_user_data(reg_data: RegistrationData) -> dict[str, Any]:
    yield {
        key: value for key, value in reg_data.items() if not key.startswith('password')
    }


@pytest.fixture()
def expected_serialized_user(reg_data: RegistrationData) -> dict[str, Any]:
    yield {
        'name': reg_data['first_name'],
        'last_name': reg_data['last_name'],
        'birthday': reg_data['date_of_birth'].strftime('%d.%m.%Y'),
        'city_of_birth': reg_data['address'],
        'position': reg_data['job_title'],
        'email': reg_data['email'],
        'phone': reg_data['phone'],
    }


@pytest.fixture()
def user(
    expected_user_data: RegistrationData,
) -> User:
    yield User.objects.create(**expected_user_data)
