from typing import final

import pydantic
import requests

from server.common import pydantic_model
from server.common.services import http


@final
class PictureResponse(pydantic_model.BaseModel):
    """Schema for API response with :term:`picture` items."""

    id: int
    url: str


# TODO: use redis-based caching
@final
class PicturesFetch(http.BaseFetcher):
    """Service around fetching pictures from :term:`Placeholder API`."""

    _url_path = '/photos'

    def __call__(
        self,
        *,
        limit: int,
    ) -> list[PictureResponse]:
        """Create remote user and return assigned ids."""
        response = requests.get(
            self.url_path(),
            params={'_limit': limit},
            timeout=self._api_timeout,
        )
        response.raise_for_status()
        return pydantic.TypeAdapter(
            list[PictureResponse],
        ).validate_json(
            response.text,
        )
