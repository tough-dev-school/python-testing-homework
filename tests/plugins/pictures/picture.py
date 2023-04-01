from typing import TypedDict, final


@final
class FavouritePictureData(TypedDict):
    # special
    foreign_id: int
    url: str