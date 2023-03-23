import datetime
from typing import final, Callable, Protocol, TypedDict
from typing_extensions import Unpack

from mimesis.schema import Field, Schema
import pytest

from server.apps.identity.models import User


USER_BIRTHDAY_FORMAT = '%Y-%m-%d'


@final
class ProfileData(TypedDict, total=False):
    first_name: str
    last_name: str
    date_of_birth: str
    address: str
    job_title: str
    phone: str


@final
class ProfileDataFactory(Protocol):
    def __call__(self, **fields: Unpack[ProfileData]) -> ProfileData:
        """Profile data factory protocol."""


@pytest.fixture
def mf() -> Field:
    return Field()


@pytest.fixture
def user_profile_data_factory(mf) -> ProfileDataFactory:
    schema = Schema(
        schema=lambda: {
            'first_name': mf('person.first_name'),
            'last_name': mf('person.last_name'),
            'date_of_birth': mf(
                'datetime.formatted_date',
                fmt=USER_BIRTHDAY_FORMAT,
                end=datetime.date.today().year - 1,
            ),
            'address': mf('address.address'),
            'job_title': mf('person.occupation'),
            'phone': mf('person.telephone'),
        }
    )
    return lambda **fields: (schema * 1)[0] | fields


@pytest.fixture
def user_profile_data(user_profile_data_factory: ProfileDataFactory) -> ProfileData:
    return user_profile_data_factory()


ProfileAssertion = Callable[[User, ProfileData], None]


@pytest.fixture
def assert_user_profile() -> ProfileAssertion:
    def _assert(user: User, profile_data: ProfileData):
        assert user.first_name == profile_data['first_name']
        assert user.last_name == profile_data['last_name']
        if user.date_of_birth:
            assert (
                user.date_of_birth.strftime(USER_BIRTHDAY_FORMAT)
                == profile_data['date_of_birth']
            )
        else:
            assert not profile_data['date_of_birth']
        assert user.address == profile_data['address']
        assert user.job_title == profile_data['job_title']
        assert user.phone == profile_data['phone']

    return _assert


@pytest.fixture
def user_email(mf) -> str:
    return mf('person.email', unique=True)


@pytest.fixture
def user_password(mf) -> str:
    return mf('person.password')
