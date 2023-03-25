from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db()
@pytest.mark.parametrize(('url', 'template'), [
    ('identity:login', 'identity/pages/login.html'),
    ('identity:registration', 'identity/pages/registration.html'),
])
def test_pages(
    client: Client,
    url: str,
    template: str,
) -> None:
    """Test the pages."""
    response = client.get(reverse(url))

    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, template)  # type: ignore[arg-type]


@pytest.mark.django_db()
def test_user_update_page(logged_in_client: Client) -> None:
    """Test the user update page."""
    response = logged_in_client.get(reverse('identity:user_update'))

    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(
        response,  # type: ignore[arg-type]
        'identity/pages/user_update.html',
    )
