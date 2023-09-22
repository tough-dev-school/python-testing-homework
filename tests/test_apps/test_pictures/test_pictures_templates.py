import pytest
from django.http import HttpResponse
from django.shortcuts import render
from django.test import RequestFactory

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture()
def favourite_pictures(mixer):
    """Exists favourite pictures."""
    return mixer.cycle(5).blend('pictures.FavouritePicture')


def test_registration(favourite_pictures):
    """Test register favourite picture template."""
    page = render(
        RequestFactory().get('/pictures/favourites'),
        'pictures/pages/favourites.html',
        {
            'object_list': favourite_pictures,
        },
    )

    assert isinstance(page, HttpResponse)


def test_index():
    """Test index page template."""
    page = render(
        RequestFactory().get('/pictures'),
        'pictures/pages/index.html',
    )

    assert isinstance(page, HttpResponse)
