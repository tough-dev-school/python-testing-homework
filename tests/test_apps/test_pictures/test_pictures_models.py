import pytest


@pytest.mark.django_db
def test_favourite_picture(
    picture_factory,
    assert_favourite_picture
) -> None:
    favourite_picture = picture_factory()[0]
    assert_favourite_picture(
        favourite_picture=favourite_picture,
        expected=favourite_picture.__dict__
    )

