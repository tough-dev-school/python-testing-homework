import pytest

from tests.plugins.identity.registration import (
    RegistrationData,
    RegistrationDataFactory,
    UserData,
)

USER_REGISTRATION_REQUIRED_FIELDS = (
    'email',
    'first_name',
    'last_name',
    'address',
    'job_title',
    'phone',
)


@pytest.fixture()
def registration_data_without_password(
    registration_data: RegistrationData,
) -> RegistrationData:
    """Registration data with empty passwords fields."""
    registration_data['password1'] = ''
    registration_data['password2'] = ''
    return registration_data


@pytest.fixture()
def registration_data_empty_birth_date(
    registration_data: RegistrationData,
) -> RegistrationData:
    """Registration data with empty date of birth."""
    registration_data['date_of_birth'] = ''
    return registration_data


@pytest.fixture(params=USER_REGISTRATION_REQUIRED_FIELDS)
def registration_data_without_req_field(
    registration_data_factory: RegistrationDataFactory,
    request: pytest.FixtureRequest,
) -> RegistrationData:
    """Parametrized registration data with 1 missing required field."""
    field = request.param
    return registration_data_factory(**{field: ''})


@pytest.fixture()
def user_data_empty_birth_date(
    registration_data_empty_birth_date: RegistrationData,
) -> UserData:
    """User data with empty date of birth."""
    return {  # type: ignore[return-value]
        key_name: value_part
        for key_name, value_part in registration_data_empty_birth_date.items()
        if not key_name.startswith('password')
    }
