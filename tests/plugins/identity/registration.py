import json
from typing import TYPE_CHECKING, Callable, Generator, Protocol, final

import httpretty
import pytest
import requests
from mimesis.locales import Locale
from mimesis.schema import Field, Schema
from typing_extensions import Unpack

if TYPE_CHECKING:
    from plugins.identity.user import (
        ExternalAPIUserResponse,
        RegistrationData,
        UserData,
    )


@final
class RegistrationDataFactory(Protocol):
    """Registration data factory protocol."""

    def __call__(
        self,
        **fields: Unpack['RegistrationData'],
    ) -> 'RegistrationData':
        """User registration data factory protocol."""


@pytest.fixture()
def registration_data_factory(faker_seed: int) -> RegistrationDataFactory:
    """Returns factory for fake random data for registration."""

    def factory(**fields: Unpack['RegistrationData']) -> 'RegistrationData':
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
            **{'password1': password, 'password2': password},
            **fields,
        }

    return factory


@pytest.fixture()
def registration_data(
    registration_data_factory: RegistrationDataFactory,
) -> 'RegistrationData':
    """Returns fake random user data for user registration."""
    return registration_data_factory()


@pytest.fixture()
def external_api_user_response(
    user_data: 'UserData',
    external_api_url_factory: Callable[[str], str],
) -> 'ExternalAPIUserResponse':
    """Post user to external JSON Server API and get it back in response."""
    date_of_birth = user_data['date_of_birth']
    user_data['date_of_birth'] = date_of_birth.strftime('%d.%m.%Y')
    connection_limit_in_sec = 2
    execution_limit_in_sec = 5
    return requests.post(
        url=external_api_url_factory('users'),
        timeout=(connection_limit_in_sec, execution_limit_in_sec),
        json=user_data,
    ).json()


@pytest.fixture()
def external_api_user_response_mock(
    user_data: 'UserData',
    faker_seed: int,
) -> 'ExternalAPIUserResponse':
    """Create fake external api response for external `/user/register` calls."""
    mf = Field(locale=Locale.RU, seed=faker_seed)
    schema = Schema(schema=lambda: {
        'id': str(mf('numeric.increment')),
        **user_data,
    })
    return schema.create(iterations=1)[0]


@pytest.fixture()
def external_api_user_call_mock(
    external_api_url_factory: Callable[[str], str],
    external_api_user_response_mock,
) -> Generator['ExternalAPIUserResponse', None, None]:
    """Mock external `/user/register` calls."""
    date_of_birth = external_api_user_response_mock['date_of_birth']
    external_api_user_response_mock['date_of_birth'] = str(date_of_birth)
    with httpretty.httprettized():
        httpretty.register_uri(
            method=httpretty.POST,
            uri=external_api_url_factory('users'),
            body=json.dumps(external_api_user_response_mock),
        )
        yield external_api_user_response_mock

        assert httpretty.has_request()
        assert httpretty.last_request().method == 'POST'
        assert httpretty.last_request().path == '/users'
