import pytest
from mimesis import Field, Schema
from mimesis.enums import Locale

from server.apps.identity.models import User
from tests.plugins.identity.user import RegistrationData, UserAssertion


@pytest.fixture()
def user_data_factory():
    """Fabricate user data."""

    def factory(faker_seed, **fields) -> RegistrationData:
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
            **{'password': password},
            **fields,
        }

    return factory


@pytest.fixture()
def user_data(user_data_factory, faker_seed):
    """Random user data from factory."""
    return user_data_factory(faker_seed)


@pytest.fixture()
def registration_data(user_data: RegistrationData) -> RegistrationData:
    """User data with passwords for registration"""
    user_data['password1'] = user_data['password']
    user_data['password2'] = user_data['password']

    return user_data


@pytest.fixture(scope='session')
def assert_correct_user() -> UserAssertion:
    """Check that user created correctly."""

    def factory(expected: RegistrationData) -> None:
        user = User.objects.get(email=expected['email'])
        # Special fields:
        assert user.id
        assert user.is_active
        assert not user.is_superuser
        assert not user.is_staff
        # All other fields:
        for field_name, data_value in expected.items():
            if not field_name.startswith('password'):
                assert getattr(user, field_name) == data_value

    return factory
