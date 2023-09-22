import pytest

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture()
def favour_picture(mixer, exists_user):
    """Favourite picture."""
    return mixer.blend(
        'pictures.FavouritePicture',
        user_id=exists_user.id,
        foreign_id=10,
    )


def test_str(favour_picture, exists_user):
    """Test FavouritePicture string representation."""
    assert str(favour_picture) == '<Picture 10 by {0}>'.format(exists_user.id)
