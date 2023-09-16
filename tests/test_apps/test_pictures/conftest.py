import pytest


@pytest.fixture
def create_two_favourite_picture(
    picture_factory,
    favourite_picture_data
) -> int:
    # Странно получать из create_two_favourite_picture user_id
    favourite_picture = picture_factory(favourite_picture_data)
    second_picture_data = favourite_picture_data
    second_picture_data['foreign_id'] = 2
    picture_factory(second_picture_data)
    return favourite_picture.user_id
