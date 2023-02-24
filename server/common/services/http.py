from typing import ClassVar
from urllib.parse import urljoin

from attr import dataclass


@dataclass(frozen=True, slots=True)
class BaseFetcher(object):
    """Base class for our HTTP actions."""

    #: Dependencies:
    _api_url: str
    _api_timeout: int

    #: This must be defined in all subclasses:
    _url_path: ClassVar[str]

    def url_path(self) -> str:
        """Full URL for the request."""
        return urljoin(self._api_url, self._url_path)
