from http import HTTPStatus

import pytest
from django.test import Client


@pytest.mark.django_db()
def test_favourites_retrieval(user_client: Client) -> None:
    response = user_client.get('/pictures/favourites')

    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db()
def test_favourites_requires_login(
    client: Client,
    favourites_endpoint: str,
) -> None:
    response = client.get(favourites_endpoint)

    assert response.status_code == HTTPStatus.FOUND
    assert response['Location'] == '/identity/login?next=' + favourites_endpoint
