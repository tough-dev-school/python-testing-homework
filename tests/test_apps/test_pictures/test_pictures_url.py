from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
def test_dashboard_view(
    client: Client,
    create_two_favourite_picture
) -> None:
    create_two_favourite_picture
    response = client.get(
        '/pictures/dashboard'
    )
    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db
def test_favourite_picture(
    client: Client,
    create_two_favourite_picture
) -> None:
    create_two_favourite_picture
    response = client.get(
        '/pictures/favourites'
    )
    assert response.status_code == HTTPStatus.FOUND
