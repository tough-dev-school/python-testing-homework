from http import HTTPStatus

import pytest

from server.apps.pictures.models import FavouritePicture

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture()
def existed_picture(exists_user, mixer):
    return mixer.blend('pictures.FavouritePicture', user=exists_user)


def test_get(user_client):
    """Test get pictures dashboard."""
    got = user_client.get('/pictures/dashboard')

    assert got.status_code == HTTPStatus.OK


def test_create(user_client, exists_user):
    """Test add picture to favourite."""
    got = user_client.post('/pictures/dashboard', data={
        'foreign_id': 1,
        'url': 'https://via.placeholder.com/600/92c952',
    })

    assert got.status_code == HTTPStatus.FOUND
    assert got.headers['location'] == '/pictures/dashboard'
    assert FavouritePicture.objects.filter(
        user_id=exists_user.id,
        foreign_id=1,
        url='https://via.placeholder.com/600/92c952',
    ).count() == 1


@pytest.mark.usefixtures()
def test_delete(user_client, exists_user, existed_picture):
    """Test delete picture from favourite."""
    got = user_client.delete('/pictures/favourites/{0}'.format(existed_picture.id))

    assert got.status_code == HTTPStatus.FOUND
    assert got.headers['location'] == '/pictures/dashboard'
    assert FavouritePicture.objects.count() == 0


def test_get_favourites(user_client):
    """Test get favourite pictures."""
    got = user_client.get('/pictures/favourites')

    assert got.status_code == HTTPStatus.OK
