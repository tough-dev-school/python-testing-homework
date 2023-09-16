from http import HTTPStatus

import pytest
from django.test import Client


@pytest.mark.django_db()
@pytest.mark.parametrize(('url_to_check', 'expected_status'), [
    ('/pictures/dashboard', HTTPStatus.FOUND),
    ('/pictures/favourites', HTTPStatus.FOUND),
])
def test_urls(
    client: Client, url_to_check: str, expected_status: HTTPStatus,
) -> None:
    """Test ensures that app urls are accessible."""
    response = client.get(url_to_check)

    assert response.status_code == expected_status
