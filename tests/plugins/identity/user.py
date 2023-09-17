from datetime import datetime
from typing import Callable, Protocol, TypeAlias, TypedDict, Unpack, final

import pytest
from mimesis.locales import Locale
from mimesis.schema import Field, Schema

from server.apps.identity.models import User


class UserData(TypedDict, total=False):
    email: str
    first_name: str
    last_name: str
    date_of_birth: datetime
    address: str
    job_title: str
    phone: str
    phone_type: int


UserAssertion: TypeAlias = Callable[[str, UserData], None]


@final
class RegistrationData(UserData, total=False):
    password1: str
    password2: str


@final
class RegistrationDataFactory(Protocol):  # type: ignore[misc]
    def __call__(self, **fields: Unpack[RegistrationData]) -> RegistrationData:
        """User registration data factory."""


@pytest.fixture(scope="session")
def assert_correct_user() -> UserAssertion:
    def factory(email: str, expected: UserData) -> None:
        user = User.objects.get(email=email)
        assert user.id
        assert user.is_active
        assert not user.is_superuser
        assert not user.is_staff
        for field_name, data_value in expected.items():
            assert getattr(user, field_name) == data_value

    return factory


@pytest.fixture(scope='function')
def registration_data_factory(faker_seed: int) -> RegistrationDataFactory:
    def factory(**fields: Unpack[RegistrationData]) -> RegistrationData:
        mf = Field(locale=Locale.RU, seed=faker_seed)
        password = mf('password')
        schema = Schema(schema=lambda: {
            'email': mf('person.email'),
            'first_name': mf('person.first_name'),
            'last_name': mf('person.last_name'),
            'date_of_birth': mf('datetime.date'),
            'job_title': mf('person.occupation'),
            'phone': mf('person.telephone'),
            'phone_type': mf('choice', items=[1, 2, 3]),
        }, iterations=1)
        return {
            **next(schema),  # type: ignore[typeddict-item]
            **{'password1': password, 'password2': password},
            **fields
        }

    return factory
