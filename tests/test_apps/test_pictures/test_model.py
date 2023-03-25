import pytest

from server.apps.pictures.models import FavouritePicture

fake_picture_data = [
    (1, 2, '<Picture 1 by 2>'),
    (2, 1, '<Picture 2 by 1>'),
]


@pytest.mark.parametrize(('foreign', 'user', 'exp_string'), fake_picture_data)
def test_picture_string_representation(foreign, user, exp_string):
    """Checks the correct representation of the picture as string."""
    picture = FavouritePicture(
        foreign_id=foreign,
        user_id=user,
    )

    assert str(picture) == exp_string
