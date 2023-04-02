from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.intrastructure.django.forms import UserUpdateForm
from server.apps.identity.models import User
from tests.plugins.constants import EXPECTED_LEAD_ID_FINAL

if TYPE_CHECKING:
    from tests.plugins.identity.user import RegistrationDataFactory


@pytest.mark.django_db()
@pytest.mark.parametrize('field', User.REQUIRED_FIELDS + [User.USERNAME_FIELD])
def test_registration_missing_required_field(
    client: Client,
    registration_data_factory: 'RegistrationDataFactory',
    field: str,
) -> None:
    """Test that missing required will fail the registration."""
    post_data = registration_data_factory(
        **{field: ''},  # type: ignore[arg-type]
    )

    response = client.post(
        reverse('identity:registration'),
        data=post_data,
    )

    assert response.status_code == HTTPStatus.OK
    assert not User.objects.filter(email=post_data['email'])


@pytest.mark.django_db()
def test_success_registration(
    client: Client,
    registration_data_factory: 'RegistrationDataFactory',
) -> None:
    """Test success registration."""
    post_data = registration_data_factory()

    response = client.post(
        reverse('identity:registration'),
        data=post_data,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert User.objects.filter(email=post_data['email'])


@pytest.mark.django_db()
@pytest.mark.parametrize('field', User.REQUIRED_FIELDS)
def test_success_user_update(
    client: Client,
    field: str,
    user_registration: User,
    registration_random_data_factory: 'RegistrationDataFactory',
) -> None:
    """Test success updating."""
    post_data = registration_random_data_factory()
    form = UserUpdateForm(instance=user_registration).initial
    form[field] = post_data[field]  # type: ignore[index]

    response = client.post(
        reverse('identity:user_update'),
        data=form,
        follow=True,
    )

    users = User.objects.filter(email=user_registration.email)
    actual_value = users.values_list(field, flat=True).first()
    assert response.status_code == HTTPStatus.OK
    assert actual_value == post_data[field]


@pytest.mark.django_db()
@pytest.mark.timeout(4)
@pytest.mark.usefixtures('_apply_json_server')
def test_external_service(
    client: Client,
    registration_data_factory: 'RegistrationDataFactory',
) -> None:
    """Test pictures placeholder with json-server."""
    post_data = registration_data_factory()

    response = client.post(
        reverse('identity:registration'),
        data=post_data,
    )
    user = User.objects.get(email=post_data['email'])

    assert response.status_code == HTTPStatus.FOUND
    assert user.lead_id == EXPECTED_LEAD_ID_FINAL
