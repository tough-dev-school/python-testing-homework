import datetime
from typing import Any, Callable, Mapping

from mimesis.schema import Field, Schema
import pytest

from server.apps.identity.models import User


USER_BIRTHDAY_FORMAT = '%Y-%m-%d'


@pytest.fixture(scope='session')
def mimesis_field() -> Field:
    return Field()


@pytest.fixture(scope='session')
def user_profile_schema(mimesis_field) -> Schema:
    return Schema(
        schema=lambda: {
            'first_name': mimesis_field('person.first_name'),
            'last_name': mimesis_field('person.last_name'),
            'date_of_birth': mimesis_field(
                'datetime.formatted_date',
                fmt=USER_BIRTHDAY_FORMAT,
                end=datetime.date.today().year - 1,
            ),
            'address': mimesis_field('address.address'),
            'job_title': mimesis_field('person.occupation'),
            'phone': mimesis_field('person.telephone'),
        }
    )


@pytest.fixture
def assert_user_profile() -> Callable[[User, Mapping[str, Any]], None]:
    def _assert_user_profile(user: User, profile_data: Mapping[str, Any]):
        assert user.first_name == profile_data['first_name']
        assert user.last_name == profile_data['last_name']
        assert (
            user.date_of_birth.strftime(USER_BIRTHDAY_FORMAT)
            == profile_data['date_of_birth']
        )
        assert user.address == profile_data['address']
        assert user.job_title == profile_data['job_title']
        assert user.phone == profile_data['phone']

    return _assert_user_profile


@pytest.fixture
def user_profile_data(user_profile_schema: Schema) -> Mapping[str, Any]:
    return (user_profile_schema * 1)[0]


@pytest.fixture
def user_email(mimesis_field: Field) -> str:
    return mimesis_field('person.email', unique=True)


@pytest.fixture
def user_password(mimesis_field: Field) -> str:
    return mimesis_field('person.password')
