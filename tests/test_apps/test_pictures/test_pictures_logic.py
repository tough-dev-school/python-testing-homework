import pytest

from server.apps.pictures.logic.repo.queries import favourite_pictures
from server.apps.pictures.logic.usecases.favourites_list import FavouritesList


@pytest.mark.django_db
@pytest.mark.parametrize(
    'cycle_number',
    [1, 3, 9]
)
def test_by_user(
    picture_factory,
    cycle_number
) -> None:
    
    pictures = picture_factory(cycle_number)
    user_id = pictures[0].user_id
    queryset = favourite_pictures.by_user(
        user_id=user_id)
    assert len(queryset) == cycle_number


@pytest.mark.django_db
@pytest.mark.parametrize(
    'cycle_number',
    [1, 3, 7]
)
def test_favourites_list(
    picture_factory,
    cycle_number
) -> None:
    
    pictures = picture_factory(cycle_number)
    user_id = pictures[0].user_id
    favorites_list = FavouritesList()
    assert len(favorites_list(user_id)) == cycle_number
