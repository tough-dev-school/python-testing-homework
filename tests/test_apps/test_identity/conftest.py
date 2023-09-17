from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from tests.plugins.identity.user import (
        RegistrationData,
        RegistrationDataFactory,
        UserData,
    )


@pytest.fixture
def valid_registration_data(
    registration_data_factory: 'RegistrationDataFactory'
) -> 'RegistrationData':
    return registration_data_factory()


@pytest.fixture()
def valid_user_data(valid_registration_data: 'RegistrationData') -> 'UserData':
    return {  # type: ignore[return-value]
        key_name: value_part
        for key_name, value_part in valid_registration_data.items()
        if not key_name.startswith('password')
    }
