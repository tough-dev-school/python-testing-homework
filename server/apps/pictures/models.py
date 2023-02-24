from typing import final

from django.conf import settings
from django.db import models

from server.common.django.models import TimedMixin


@final
class FavouritePicture(TimedMixin, models.Model):
    """Represents a :term:`picture` saved in :term:`favourites`."""

    # Linking:
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='pictures',
        on_delete=models.CASCADE,
    )

    # Data:
    foreign_id = models.IntegerField()
    url = models.URLField()

    def __str__(self) -> str:
        """Beatuful representation."""
        return '<Picture {0} by {1}>'.format(self.foreign_id, self.user_id)
