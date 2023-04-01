from typing import Protocol, TypedDict

import pytest
from mimesis.schema import Field, Schema
from typing_extensions import Unpack


class PictureData(TypedDict, total=False):
    """Favorite picture schema."""

    foreign_id: int
    url: str


class ExternalAPIPictureData(TypedDict, total=False):
    """Picture data in external JSON Server."""

    id: int
    url: str


class PictureDataFactory(Protocol):
    """Favorite picture data factory protocol."""

    def __call__(self, **fields: Unpack[PictureData]) -> PictureData:
        """Return picture data on call."""


@pytest.fixture()
def picture_data_factory(fake_field: Field) -> PictureDataFactory:
    """Factory for fake random picture data."""

    def factory(**fields: Unpack[PictureData]) -> PictureData:
        schema = Schema(
            schema=lambda: {
                'foreign_id': fake_field('integer_number'),
                'url': fake_field('url'),
            },
        )
        return {
            **schema.create(iterations=1)[0],  # type: ignore[misc]
            **fields,
        }

    return factory
