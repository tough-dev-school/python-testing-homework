from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
def test_dashboard_view(
    client: Client,
    picture_factory
) -> None:
    picture_factory
    response = client.get(
        '/pictures/dashboard'
    )
    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db
def test_favourite_picture(
    client: Client,
    picture_factory
) -> None:
    picture_factory
    response = client.get(
        '/pictures/favourites'
    )
    assert response.status_code == HTTPStatus.FOUND
