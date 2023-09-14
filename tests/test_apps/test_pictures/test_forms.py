import pytest
from mixer.backend.django import mixer

from server.apps.pictures.intrastructure.django.forms import FavouritesForm
from server.apps.pictures.models import FavouritePicture

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def picture():
    yield mixer.blend(FavouritePicture)


@pytest.fixture
def picture_raw_data(picture):
    yield {"foreign_id": picture.foreign_id, "url": picture.url}


@pytest.mark.parametrize(
    "save, expected", [
        (True, 2),
        (False, 1)
    ]
)
def test_favourites_form_correct_with_user(user, picture_raw_data, save, expected):
    form = FavouritesForm(data=picture_raw_data, user=user)
    form.save(save)
    assert form.is_valid()
    assert FavouritePicture.objects.count() == expected


def test_favourites_form_fail_without_user(picture_raw_data):
    with pytest.raises(KeyError):
        FavouritesForm(data=picture_raw_data)

    """expected count == 1 because picture fixture create one record, but form doesn't create"""
    assert FavouritePicture.objects.count() == 1
