import pytest

from server.apps.pictures.models import FavouritePicture

favourite_picture_params = [
    (1234567890, 'some_test_foreign_id'),
    (1234567890, None),
    (None, 'some_test_foreign_id'),
    (None, None),
]


@pytest.mark.parametrize(('foreign_id', 'user_id'), favourite_picture_params)
@pytest.mark.django_db()
def test_output_correct_str(foreign_id, user_id):
    """Test that string representation is correct."""
    string_format = FavouritePicture(foreign_id=foreign_id, user_id=user_id)

    assert str(string_format) == f'<Picture {foreign_id} by {user_id}>'
