from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User
from tests.plugins.identity.user_update import UserUpdateData
from tests.test_apps.test_identity.conftest import (
    FieldMissingAssertion,
    UserAssertion,
)


@pytest.mark.django_db()
def test_not_logined_redirect(client: Client) -> None:
    """Endpoint redirects if user is not logined."""
    response = client.get(path=reverse('identity:user_update'))
    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db()
def test_page_renders(client_logined: Client) -> None:
    """Basic `get` method works if user is logined."""
    response = client_logined.get(path=reverse('identity:user_update'))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db()
def test_update_no_required_field(
    client_logined: Client,
    user_update_data_without_req_field: UserUpdateData,
    assert_field_missing: FieldMissingAssertion,
) -> None:
    """User update fails is any required field is not provided."""
    response = client_logined.post(
        path=reverse('identity:user_update'),
        data=user_update_data_without_req_field,
    )
    assert response.status_code == HTTPStatus.OK
    assert_field_missing(response.content)


@pytest.mark.django_db()
def test_update_valid(
    client_logined: Client,
    user_update_data: UserUpdateData,
    db_user: User,
    assert_correct_user: UserAssertion,
) -> None:
    """User update is successful if all required fields are provided."""
    response = client_logined.post(
        path=reverse('identity:user_update'),
        data=user_update_data,
    )
    assert response.status_code == HTTPStatus.FOUND
    assert_correct_user(db_user.email, user_update_data)
