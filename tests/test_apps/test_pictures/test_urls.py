import pytest
from django.test import Client
from django.urls import reverse
from http import HTTPStatus


@pytest.mark.django_db()
@pytest.mark.parametrize(('checking_url', 'expected_http_status'), [
    ('pictures:dashboard', HTTPStatus.FOUND),
    ('pictures:favourites', HTTPStatus.FOUND),
])
def test_urls(
    client: Client, checking_url: str, expected_http_status: HTTPStatus,
) -> None:
    response = client.get(reverse(checking_url))
    assert response.status_code == expected_http_status