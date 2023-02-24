from django.db.models import QuerySet

from server.apps.pictures.models import FavouritePicture


def by_user(user_id: int) -> QuerySet[FavouritePicture]:
    """Search :class:`FavouritePicture` by user id."""
    # TODO: this should be limited and probably paginated
    return FavouritePicture.objects.filter(user_id=user_id)
