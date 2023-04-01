from typing import Callable

import pytest
import requests
from typing_extensions import TypeAlias

from config.settings import SETTINGS
from server.apps.identity.models import User
from tests.plugins.identity.registration import (
    ExternalAPIUserData,
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


ExternalAPIUserAssertion: TypeAlias = Callable[
    [ExternalAPIUserData, UserData],
    None,
]


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


@pytest.fixture()
def user_external_api(
    registration_data: RegistrationData,
) -> ExternalAPIUserData:
    """Post user to external JSON Server API and get it back in response."""
    registration_data['date_of_birth'] = str(registration_data['date_of_birth'])
    return requests.post(
        url=SETTINGS.JSON_SERVER_USERS_URL,
        timeout=SETTINGS.JSON_SERVER_TIMEOUT,
        json=registration_data,
    ).json()


@pytest.fixture(scope='session')
def assert_correct_user_external_api() -> ExternalAPIUserAssertion:
    """Assert that user data in external API is the same as expected one."""

    def factory(
        user_external_api: ExternalAPIUserData,
        expected: UserData,
    ) -> None:
        assert user_external_api['id']
        for field_name, data_value in expected.items():
            if field_name == User.DATE_OF_BIRTH_FIELD:
                data_value = str(data_value)  # noqa: WPS 440
            assert user_external_api[field_name] == data_value

    return factory
