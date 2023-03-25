import pytest

from server.apps.pictures.models import FavouritePicture

fake_picture_data = [
    [1, 2, '<Picture 1 by 2>'],
    [2, 1, '<Picture 2 by 1>']
]


@pytest.mark.parametrize('foreign_id, user_id, expected_string', fake_picture_data)
def test_picture_string_representation(foreign_id, user_id, expected_string):
    picture = FavouritePicture(
        foreign_id=foreign_id,
        user_id=user_id
    )

    assert str(picture) == expected_string
