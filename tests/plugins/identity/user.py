import factory
import pytest
from django.contrib.auth.hashers import make_password
from factory.base import FactoryMetaClass
from pytest_factoryboy import register

from server.apps.identity.models import User

locale = "RU_ru"


@register
class UserDataFactory(factory.DictFactory):
    email = factory.Faker("email")
    first_name = factory.Faker("first_name", locale=locale)
    last_name = factory.Faker("last_name", locale=locale)
    date_of_birth = factory.Faker("date_object")
    address = factory.Faker("address", locale=locale)
    job_title = factory.Faker("job", locale=locale)
    phone = factory.Faker("phone_number")
    password = make_password("pass")


@register
class UserUpdateDataFactory(factory.DictFactory):
    first_name = factory.Faker("first_name", locale=locale)
    last_name = factory.Faker("last_name", locale=locale)
    date_of_birth = factory.Faker("date_object")
    address = factory.Faker("address", locale=locale)
    job_title = factory.Faker("job", locale=locale)
    phone = factory.Faker("phone_number")


@pytest.fixture()
def registration_data(user_data_factory: FactoryMetaClass) -> dict:
    data = user_data_factory()
    data["password1"] = data["password"]
    data["password2"] = data["password"]

    return data


@pytest.fixture()
def expected_user_data() -> dict:
    def factory(data: dict) -> dict:
        return {
            key_name: value_part
            for key_name, value_part in data.items()
            if not key_name.startswith("password")
        }

    return factory


@pytest.fixture()
def user(user_data_factory: FactoryMetaClass) -> User:
    return User.objects.create_user(**user_data_factory())


@pytest.fixture(scope="session")
def assert_correct_user() -> None:
    def factory(email: str, expected: dict) -> None:
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


@pytest.fixture(scope="session")
def assert_correct_superuser() -> None:
    def factory(email: str, expected: dict) -> None:
        user = User.objects.get(email=email)
        # Special fields:
        assert user.id
        assert user.is_active
        assert user.is_superuser
        assert user.is_staff
        # All other fields:
        for field_name, data_value in expected.items():
            assert getattr(user, field_name) == data_value

    return factory
