import datetime
from typing import Callable, Protocol, TypedDict, Callable, final
from typing_extensions import Unpack, TypeAlias

import pytest
from mimesis.schema import Field, Schema

from server.apps.identity.models import User


USER_BIRTHDAY_FORMAT = '%Y-%m-%d'


class UserData(TypedDict, total=False):
    """
    Represent the simplified user data that is required to create a new user.
    It does not include ``password``, because it is very special in django.
    Importing this type is only allowed under ``if TYPE_CHECKING`` in tests.
    """
    email: str
    first_name: str
    last_name: str
    date_of_birth: datetime.datetime
    address: str
    job_title: str
    phone: str


@final
class RegistrationData(UserData, total=False):
    """
    Represent the registration data that is required to create a new user.
    Importing this type is only allowed under ``if TYPE_CHECKING`` in tests.
    """
    password1: str
    password2: str


@final
class RegistrationDataFactory(Protocol):
    def __call__(
        self,
        **fields: Unpack[RegistrationData],
    ) -> RegistrationData:
        """User data factory protocol."""


@pytest.fixture()
def mf(faker_seed: int) -> Field:
    """Returns the current mimesis `Field`."""

    return Field(seed=faker_seed)


@pytest.fixture()
def registration_data_factory(
    mf: Field,
) -> RegistrationDataFactory:
    """Returns factory for fake random data for regitration."""

    def factory(**fields: Unpack[RegistrationData]) -> RegistrationData:
        password = mf('password') # by default passwords are equal
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
            **schema.create(iterations=1)[0], # type: ignore[misc]
            **{'password1': password, 'password2': password},
            **fields,
        }
    return factory


@pytest.fixture()
def registration_data(
    registration_data_factory: RegistrationDataFactory,
) -> RegistrationData:
    """Default success registration data."""
    return registration_data_factory()


UserAssertion: TypeAlias = Callable[[str, UserData], None]


@pytest.fixture(scope='session')
def assert_correct_user() -> UserAssertion:
    def factory(email: str, expected: UserData) -> None:
        user = User.objects.get(email=email)
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
def user_data(registration_data: 'RegistrationData') -> 'UserData':
    """
    We need to simplify registration data to drop passwords.
    Basically, it is the same as ``registration_data``, but without passwords.
    """

    return { # type: ignore[return-value]
        key_name: value_part
        for key_name, value_part in registration_data.items()
        if not key_name.startswith('password')
    }


@pytest.fixture()
def user_email(mf) -> str:
    """Email of the current user."""
    return mf('person.email')


@pytest.fixture()
def default_password(mf) -> str:
    """Default password for user factory."""
    return mf('person.password')


@pytest.fixture()
def user_password(default_password) -> str:
    """Password of the current user."""
    return default_password






# RegistrationAssertion = Callable[[User, RegistrationData], None]



# @pytest.fixture()
# def assert_correct_user() -> RegistrationAssertion:
#     """Checks if `ProfileData` corresponds to the given `User` instance."""
#     def factory(user: User, profile_data: RegistrationData):
#         assert user.first_name == profile_data['first_name']
#         assert user.last_name == profile_data['last_name']
#         if user.date_of_birth:
#             formatted_date_of_birth = user.date_of_birth.strftime(
#                 USER_BIRTHDAY_FORMAT,
#             )
#             assert formatted_date_of_birth == profile_data['date_of_birth']
#         else:
#             assert not profile_data['date_of_birth']
#         assert user.address == profile_data['address']
#         assert user.job_title == profile_data['job_title']
#         assert user.phone == profile_data['phone']
#     return factory








# @final
# class UserFactory(Protocol):  # type: ignore[misc]
#     """A factory to generate a `User` instance."""

#     def __call__(self, **fields) -> User:
#         """Profile data factory protocol."""


# @pytest.fixture()
# def user_factory(
#     fakery: Factory[User],
#     faker_seed: int,
#     default_password: str,
# ) -> UserFactory:
#     """Creates a factory to generate a user instance."""
#     def factory(**fields):
#         password = fields.pop('password', default_password)
#         return fakery.make(  # type: ignore[call-overload]
#             model=User,
#             fields=fields,
#             seed=faker_seed,
#             pre_save=[lambda _user: _user.set_password(password)],
#         )
#     return factory


# @pytest.fixture()
# def user(
#     user_factory: UserFactory,
#     user_email: str,
#     user_password: str,
# ) -> User:
#     """The current user.
#     The fixtures `user_email` and `user_password` are used
#     as email and password of the user correspondingly.
#     """
#     return user_factory(
#         email=user_email,
#         password=user_password,
#         is_active=True,
#     )