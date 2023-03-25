import pytest
from django_fakery import factory as model_factory
from mimesis import Address, Datetime, Person
from mimesis.locales import Locale
from mimesis.schema import Schema

from protocols.identity.user import UserDict
from server.apps.identity.models import User


@pytest.fixture()
def user_factory(data_seed):
    """Data factory for user_create_new UseCase."""
    start_year: int = 1990
    end_year: int = 2000

    def factory(seed=None, **fields) -> UserDict:
        person = Person(locale=Locale.RU, seed=seed or data_seed)
        address = Address(seed=seed or data_seed)

        schema = Schema(schema=lambda: {
            'email': person.email(),
            'password': person.password().replace(':', 'f'),
            'first_name': person.first_name(),
            'last_name': person.last_name(),
            'date_of_birth': Datetime().date(start=start_year, end=end_year),
            'address': address.address(),
            'job_title': person.occupation(),
            'phone': person.telephone(mask='+7-###-###-##-##'),
        }).create(iterations=1)[0]

        return UserDict(**{**schema, **fields})

    return factory


@pytest.fixture()
def user_data(user_factory):
    """Random user data from factory."""
    return user_factory()


@pytest.fixture()
def registration_user_data(user_factory) -> UserDict:
    """User data."""
    user_data = user_factory()
    user_data['password1'] = user_data['password']
    user_data['password2'] = user_data['password']

    return user_data


@pytest.fixture()
def authed_user_data(registration_user_data) -> User:
    """Fake database user."""
    return model_factory.m(User)(**registration_user_data)


@pytest.fixture()
def db_user(user_data) -> User:
    """Database instance of user."""
    user = User(**user_data)
    user.save()
    yield user
    user.delete()


@pytest.fixture()
def update_user_data(data_seed, user_factory, authed_user_data) -> UserDict:
    """New user data for update form for current user."""
    user_data = user_factory(
        seed=data_seed, email=authed_user_data.email,
    ).items()

    return {
        field: field_value
        for field, field_value in user_data
        if not field.startswith('password')
    }


@pytest.fixture()
def login_data(user_data):
    """Data for login form."""
    return {
        'username': user_data['email'],
        'password': user_data['password'],
    }
