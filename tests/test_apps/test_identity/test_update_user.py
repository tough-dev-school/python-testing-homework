from http import HTTPStatus

import pytest

pytestmark = [
    pytest.mark.django_db,
]


def test_get(user_client):
    """Test get form for update user."""
    got = user_client.get('/identity/update')

    assert got.status_code == HTTPStatus.OK


def test_update(user_client):
    """Test update exists user."""
    got = user_client.post('/identity/update', data={
        'email': 'my@email.com',
        'first_name': 'My name',
        'last_name': 'My name',
        'date_of_birth': '1970-09-18',
        'address': 'My name',
        'job_title': 'My name',
        'phone': 'My name',
    })

    assert got.status_code == HTTPStatus.FOUND
    assert got.headers['location'] == '/identity/update'
