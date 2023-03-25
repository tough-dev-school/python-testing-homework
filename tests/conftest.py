"""
This module is used to provide configuration, fixtures, and plugins for pytest.

It may be also used for extending doctest's context:
1. https://docs.python.org/3/library/doctest.html
2. https://docs.pytest.org/en/latest/doctest.html
"""
from typing import Protocol, TypedDict, Unpack, final

import pytest
from mimesis.locales import Locale
from mimesis.schema import Field, Schema

pytest_plugins = [
    # Should be the first custom one:
    "plugins.django_settings",
    # TODO: add your own plugins here!
]


@final
class PictureData(TypedDict, total=False):
    id: int
    url: str


@final
class PictureResponseFactory(Protocol):
    def __call__(
        self,
        **fields: Unpack[PictureData],
    ) -> PictureData:
        """User data factory protocol."""


@pytest.fixture()
def picture_data_factory(
    faker_pick: int,
) -> PictureResponseFactory:
    """Returns factory for fake random data for regitration."""
    mf = Field(locale=Locale.EN, seed=faker_pick)

    def factory(count_factory: int = 1, **fields: Unpack[PictureData]) -> PictureData:
        schema = Schema(
            schema=lambda: {
                "id": mf("increment"),
                "url": mf("uri"),
            }
        )
        return [{**sh, **fields} for sh in schema * count_factory]

    return factory
