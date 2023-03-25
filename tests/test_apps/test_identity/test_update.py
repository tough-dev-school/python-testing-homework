from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User

if TYPE_CHECKING:
    from tests.plugins.identity.user import (
        UpdateUserData,
        UpdateUserDataFactory,
        UserData,
        UserUpdatedAssertion,
    )


@pytest.mark.django_db()
def test_valid_update(
    client: Client,
    db_user: 'UserData',
    updated_user_data: 'UpdateUserData',
    assert_user_updated: 'UserUpdatedAssertion',
) -> None:
    """Test that 'update' works with correct user data."""
    user = User.objects.get(email=db_user['email'])
    client.force_login(user)
    response = client.post(
        reverse('identity:user_update'),
        data=updated_user_data,
    )
    assert response.status_code == HTTPStatus.FOUND
    assert_user_updated(db_user['email'], updated_user_data)


@pytest.mark.django_db()
@pytest.mark.parametrize(
    'field',
    [
        'first_name',
        'last_name',
        'address',
        'job_title',
        'phone',
    ],
)
def test_update_missing_required_fields(
    client: Client,
    db_user: 'UserData',
    update_user_data_factory: 'UpdateUserDataFactory',
    field: str,
) -> None:
    """Test that update works with missing required fields."""
    user = User.objects.get(email=db_user['email'])
    client.force_login(user)

    updated_user_data = update_user_data_factory(**{field: ''})

    response = client.post(
        reverse('identity:user_update'),
        data=updated_user_data,
    )
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db()
def test_empty_birthday(
    client: Client,
    db_user: 'UserData',
    update_user_data_factory: 'UpdateUserDataFactory',
    assert_user_updated: 'UserUpdatedAssertion',
) -> None:
    """Test that missing date of birth will not fail registration."""
    user = User.objects.get(email=db_user['email'])
    client.force_login(user)

    post_data = update_user_data_factory(
        **{'date_of_birth': ''},  # type: ignore[arg-type]
    )

    response = client.post(
        reverse('identity:user_update'),
        data=post_data,
    )
    assert response.status_code == HTTPStatus.FOUND
    user.refresh_from_db()
    assert user.date_of_birth is None
