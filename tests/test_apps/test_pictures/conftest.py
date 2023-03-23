import pytest
from server.apps.identity.models import User
from server.apps.pictures.models import FavouritePicture


@pytest.fixture
def one_user_favourite(user: User) -> None:
    pic = FavouritePicture(user=user, foreign_id=1, url='http://bbb')
    pic.save()
    yield pic
    pic.delete()
