from typing import final

import attr

from server.apps.pictures.intrastructure.services import placeholder
from server.common.django.types import Settings


@final
@attr.dataclass(slots=True, frozen=True)
class PicturesFetch(object):
    """Fetch :term:`picture` items from :term:`Placeholder API`."""

    _settings: Settings

    def __call__(self, limit: int = 10) -> list[placeholder.PictureResponse]:
        """Update existing user in the remote api."""
        return self._fetch_pictures(limit)

    def _fetch_pictures(self, limit: int) -> list[placeholder.PictureResponse]:
        return placeholder.PicturesFetch(
            api_url=self._settings.PLACEHOLDER_API_URL,
            api_timeout=self._settings.PLACEHOLDER_API_TIMEOUT,
        )(limit=limit)
