from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User
from tests.plugins.identity.login import LoginData, LoginDataFactory
from tests.test_apps.conftest import FieldMissingAssertion

URL_PATH = reverse('identity:login')


@pytest.mark.django_db()
def test_page_renders(client: Client) -> None:
    """Basic `get` method works."""
    response = client.get(path=URL_PATH)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db()
def test_no_password(
    client: Client,
    login_data_factory: LoginDataFactory,
    assert_field_missing: FieldMissingAssertion,
) -> None:
    """Login fails if password is not provided."""
    login_data = login_data_factory(password='')  # noqa: S106
    response = client.post(path=URL_PATH, data=login_data)
    assert response.status_code == HTTPStatus.OK
    assert_field_missing(response.content)


@pytest.mark.django_db()
def test_no_username(
    client: Client,
    login_data_factory: LoginDataFactory,
    assert_field_missing: FieldMissingAssertion,
) -> None:
    """Login fails if username is not provided."""
    login_data = login_data_factory(username='')
    response = client.post(path=URL_PATH, data=login_data)
    assert response.status_code == HTTPStatus.OK
    assert_field_missing(response.content)


@pytest.mark.django_db()
def test_user_not_registered(
    client: Client,
    login_data: LoginData,
) -> None:
    """Login fails if there is no registered user for provided data."""
    response = client.post(path=URL_PATH, data=login_data)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db()
@pytest.mark.usefixtures('_mock_check_pwd')
def test_user_registered(
    client: Client,
    login_data: LoginData,
    db_user: User,
) -> None:
    """Login is successful for registered user."""
    response = client.post(path=URL_PATH, data=login_data)
    assert response.status_code == HTTPStatus.FOUND
