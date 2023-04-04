from typing import TypedDict, final


@final
class PictureData(TypedDict, total=False):
    foreign_id: int
    url: str
