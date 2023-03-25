from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse

urls_answers = [
    # user, view, expected_status

    ('client', 'pictures:dashboard', HTTPStatus.FOUND),
    ('client', 'pictures:favourites', HTTPStatus.FOUND),

    ('admin_client', 'pictures:dashboard', HTTPStatus.OK),
    ('admin_client', 'pictures:favourites', HTTPStatus.OK),
]


@pytest.mark.django_db()()
@pytest.mark.parametrize(('user', 'view', 'expected_status'), urls_answers)
def test_views_available_user(user, view, expected_status, request) -> None:
    """Accessibility of views for unauthenticated users and administrators."""
    url = reverse(view)
    current_client: Client = request.getfixturevalue(user)
    response = current_client.get(url)
    actual_status = response.status_code

    assert actual_status == expected_status
