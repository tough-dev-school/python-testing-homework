import pytest
from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer

from server.apps.identity.models import User
from server.apps.pictures.models import FavouritePicture
from server.apps.pictures.views import FavouritePicturesView

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def favorites_pictures(user):
    pics = mixer.cycle(10).blend(FavouritePicture, user=user)
    yield pics


def test_favorite_pictures_has_expected_user(user: User, favorites_pictures, request_factory: RequestFactory):
    url = reverse('pictures:favourites')
    request = request_factory.get(url)
    request.user = user

    view = FavouritePicturesView()
    view.setup(request)
    queryset = view.get_queryset()

    assert len(queryset) == len(favorites_pictures)
    for picture in queryset:
        assert picture.user == user


