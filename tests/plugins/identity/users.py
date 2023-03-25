from mimesis import Person
import pytest

from server.apps.identity.models import User


@pytest.fixture()
def user(mimesis_seed: int) -> User:
    """The current user.
    The fixtures `user_email` and `user_password` are used
    as their email and password correspondingly.
    """
    person = Person(seed=mimesis_seed)
    user = User(email=person.email(), password=person.password())
    user.save()
    return user
