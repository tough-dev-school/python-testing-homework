from faker import Faker
import pytest
from django_fakery.faker_factory import Factory
from server.apps.identity.container import container
from server.apps.identity.logic.usecases.user_create_new import UserCreateNew
from server.apps.identity.models import User


@pytest.fixture()
def user_factory(fakery: Factory[User], faker: Faker):
    """Fixture to create your own custom users. Everything is customizable."""
    def factory(user: User, password: str) -> User:
        # We store the original password for test purposes only:
        user._password = password # noqa: WPS437
        return user

    def decorator(**fields) -> User:
        password = fields.setdefault('password', faker.password())
        return fakery.m(
            User,
            post_save=[lambda user: factory(user, password)],
        )(
            **{'is_active': True, **fields},
        )
    return decorator



@pytest.mark.django_db
def test_create_user(user_factory):
    user = user_factory()

    assert user.is_active
