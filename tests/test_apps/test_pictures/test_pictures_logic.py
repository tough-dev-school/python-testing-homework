import pytest

from server.apps.pictures.logic.repo.queries import favourite_pictures
from server.apps.pictures.logic.usecases.favourites_list import FavouritesList


@pytest.mark.django_db
def test_by_user(
    create_two_favourite_picture
) -> None:
    # Недостаточная проверка
    queryset = favourite_pictures.by_user(
        user_id=create_two_favourite_picture)
    assert len(queryset) == 2


@pytest.mark.django_db
def test_favourites_list(
    create_two_favourite_picture
) -> None:
    # Недостаточная проверка
    favorites_list = FavouritesList()
    assert len(favorites_list(create_two_favourite_picture)) == 2
