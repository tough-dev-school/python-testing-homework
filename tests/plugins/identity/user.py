import pytest
import datetime as dt
from typing import Protocol, Unpack, final, TypedDict

from server.apps.identity.models import User, _UserManager


class UserData(TypedDict, total=False):
    email: str
    first_name: str
    last_name: str
    date_of_birth: dt.datetime
    address: str
    job_title: str
    phone: str
    password: str


@final
class RegistrationData(UserData):
    password1: str
    password2: str


@pytest.fixture
def user_factory():
    def factory(UserData) -> User:
        return User.objects.create(**UserData)
    return factory


@pytest.fixture
def user_model_data() -> UserData:
    '''
    можно использовать генерацию данных
    но у меня было не так много времени
    поэтому делаю как могу T_T
    проблема была в poetry
    '''
    return UserData(
        email='amongusguy@email.com',
        first_name='imposter',
        last_name='crewmate',
        date_of_birth=dt.date.today(),
        address='address',
        job_title='docker-guy',
        phone='+79991231234',
        password='123456789'
    )


@pytest.fixture
def registration_data() -> RegistrationData:
    return RegistrationData(
        email='amon@email.com',
        first_name='imposter',
        last_name='crewmate',
        date_of_birth=dt.date.today(),
        address='address',
        job_title='docker-guy',
        phone='+79991231234',
        password1='1241',
        password2='1241'
    )


@pytest.fixture
def create_user(user_factory, user_model_data) -> User:
    return user_factory(user_model_data)


@pytest.fixture
def create_superuser() -> User:
    manager = _UserManager()
    return manager.create_superuser(
        email='password@mail.com',
        password='password'
    )


@pytest.fixture(scope='session')
def assert_user():
    def factory(
            email: str,
            superuser: bool = False,
            expected: UserData | None = None
    ) -> None:
        user = User.objects.get(email=email)
        # Special fields:
        assert user.id
        assert user.is_active
        match superuser:
            case True:
                assert user.is_superuser
                assert user.is_staff
            case False:
                assert not user.is_superuser
                assert not user.is_staff
        # All other fields:
        if expected:
            for field_name, data_value in expected.items():
                assert getattr(user, field_name) == data_value
    return factory
