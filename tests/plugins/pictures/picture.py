from typing import Protocol, TypedDict, final

import pytest
from mimesis import Field, Schema
from mimesis.enums import Locale
from typing_extensions import Unpack


@final
class PictureData(TypedDict, total=False):
    """
    Represent the picture data that is required add favorite pictures.

    Importing this type is only allowed under ``if TYPE_CHECKING`` in tests.
    """

    foreign_id: int
    url: str


@final
class PictureDataFactory(Protocol):
    """Makes picture data."""

    def __call__(
        self,
        **fields: Unpack[PictureData],
    ) -> PictureData:
        """Picture data factory protocol."""
        return PictureData(**fields)


@pytest.fixture()
def picture_data_factory(
    faker_seed: int,
) -> PictureDataFactory:
    """Returns factory for fake random data for picture."""

    def factory(**fields: Unpack[PictureData]) -> PictureData:
        mf = Field(locale=Locale.RU, seed=faker_seed)
        schema = Schema(
            schema=lambda: {
                'foreign_id': mf('integer_number'),
                'url': mf('url'),
            },
        )
        return {
            **schema.create(iterations=1)[0],  # type: ignore[misc]
            **fields,
        }

    return factory


@pytest.fixture()
def picture_data(picture_data_factory) -> PictureData:
    """Creates picture data for post queries."""
    return picture_data_factory()
