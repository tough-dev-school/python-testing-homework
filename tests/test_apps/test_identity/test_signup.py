from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.test import Client
from django.urls import reverse

if TYPE_CHECKING:
    from tests.plugins.identity.pytest_identity import (
        ExpectedUserData,
        RegistrationData,
        RegistrationDataFactory,
        UserAssertion,
    )


@pytest.mark.django_db()
def test_valid_registration(
    client: Client,
    registration_data: 'RegistrationData',
    expected_user_data: 'ExpectedUserData',
    assert_correct_user: 'UserAssertion',
) -> None:
    response = client.post(
        reverse('identity:registration'),
        data=registration_data,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse('identity:login')  # type: ignore[attr-defined]
    assert_correct_user(
        registration_data['email'],
        expected_user_data(registration_data),
    )


@pytest.mark.django_db()
def test_invalid_registration_no_email(
    client: Client,
    registration_data_factory: 'RegistrationDataFactory',
) -> None:
    response = client.post(
        reverse('identity:registration'),
        data=registration_data_factory(email=''),
    )

    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db()
def test_invalid_registration_invalid_email(
    client: Client,
    registration_data_factory: 'RegistrationDataFactory',
) -> None:
    response = client.post(
        reverse('identity:registration'),
        data=registration_data_factory(email='invalid'),
    )

    assert response.status_code == HTTPStatus.OK
