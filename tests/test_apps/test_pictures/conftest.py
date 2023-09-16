import random
from typing import TypedDict, final, List, TypeAlias, Callable

import pytest
from mimesis import Field, Schema
from mimesis.enums import Locale

from server.apps.identity.models import User
from server.apps.pictures.logic.usecases.favourites_list import FavouritesList


@final
class PictureData(TypedDict, total=False):
    """Picture data."""

    id: int
    url: str


@pytest.fixture()
def picture_data() -> PictureData:
    """Picture data fixture."""

    field = Field(locale=Locale.EN, seed=random.randint(1, 1000))

    schema = Schema(schema=lambda: {
        'id': field('increment'),
        'url': field('url')
    },
                    iterations=1)

    return {**schema.create()[0]}


@pytest.fixture(params=[1, 3, 5])
def pictures_list(request) -> List:
    field = Field(locale=Locale.EN, seed=random.randint(1, 1000))

    schema = Schema(schema=lambda: {
        'id': field('increment'),
        'url': field('url')
    },
                    iterations=request.param)

    return schema.create()


FavouritePicturesAssertion: TypeAlias = Callable[[str, List[PictureData]], None]


@pytest.fixture(scope='session')
def assert_correct_favorite_pictures() -> FavouritePicturesAssertion:
    def _assert_correct_favourite_pictures(user_email: str, expected_pictures: List[PictureData]) -> None:
        true_favourite_pictures = FavouritesList()(User.objects.get(email=user_email).id).all()

        assert len(true_favourite_pictures) == len(expected_pictures)

        for i in len(expected_pictures):
            assert true_favourite_pictures[i]['id'] == expected_pictures[i]['id']
            assert true_favourite_pictures[i]['url'] == expected_pictures[i]['url']

    return _assert_correct_favourite_pictures
