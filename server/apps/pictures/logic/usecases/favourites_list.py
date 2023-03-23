from typing import final

import attr
from django.db.models import QuerySet

# NOTE: this can be a dependency as well
from server.apps.pictures.logic.repo.queries import favourite_pictures
from server.apps.pictures.models import FavouritePicture


@final
@attr.dataclass(slots=True, frozen=True)
class FavouritesList(object):
    """List :term:`favourites` pictures for a given user."""

    def __call__(self, user_id: int) -> QuerySet[FavouritePicture]:
        """Fetches favourite pictures by user."""
        return self._list_pictures(user_id)

    def _list_pictures(self, user_id: int) -> QuerySet[FavouritePicture]:
        return favourite_pictures.by_user(user_id)
