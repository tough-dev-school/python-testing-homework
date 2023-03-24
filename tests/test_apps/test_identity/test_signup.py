from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User


@pytest.mark.django_db
def test_signup(
    client: Client,
    user_credentials: 'UserCredentials',
    user_data: 'UserData',
    assert_user_was_created: 'UserAssertion'
):
    response = client.post(
        reverse("identity:registration"),
        data={**user_credentials, **user_data},
    )

    assert response.status_code == HTTPStatus.FOUND
    assert not hasattr(response.context, 'form')
    assert_user_was_created(user_credentials, user_data)


@pytest.mark.django_db
@pytest.mark.parametrize('field', User.REQUIRED_FIELDS + [User.USERNAME_FIELD])
def test_missing_required_fields(
    client: Client,
    user_credentials: 'UserCredentials',
    user_data: 'UserData',
    assert_user_was_created: 'UserAssertion',
    field: str,
):
    response = client.post(
        reverse("identity:registration"),
        data={**user_credentials, **user_data, **{field: ''}}
    )

    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_user_already_exists(
    client: Client,
    user: User,
    user_credentials: 'UserCredentials',
    user_data: 'UserData',
):

    response = client.post(
        reverse("identity:registration"),
        data={**user_credentials, **user_data, **{User.USERNAME_FIELD: user.email}},
    )
    assert len(response.context['form'].errors) >= 1
    assert response.status_code == HTTPStatus.OK
