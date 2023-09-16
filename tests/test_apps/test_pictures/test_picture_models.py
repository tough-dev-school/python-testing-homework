import pytest


@pytest.mark.django_db
def test_favourite_picture(
    picture_factory,
    favourite_picture_data,
    assert_favourite_picture
) -> None:
    favourite_picture = picture_factory(favourite_picture_data)
    assert_favourite_picture(
        favourite_picture=favourite_picture,
        expected=favourite_picture_data)

