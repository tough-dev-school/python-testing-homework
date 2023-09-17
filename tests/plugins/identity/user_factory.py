import pytest
from django_fakery.faker_factory import Factory
from faker import Faker
from mimesis import Field, Schema
from mimesis.locales import Locale

from server.apps.identity.models import User
from server.common.django.types import Settings

@pytest.fixture()
def user_factory(fakery: Factory[User], fakery: Faker) -> UserFactory:
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


@pytest.fixture()
def registration_data_factory(
	faker_seed: int,
) -> RegistrationDataFactory:
	"""Returns factory for fake random data for regitration."""
	def factory(**fields: Unpack[RegistrationData]) -> RegistrationData:
		mf = Field(locale=Locale.RU, seed=faker_seed)
        password = mf('password') # by default passwords are equal
	    schema = Schema(schema=lambda: {
			'email': mf('person.email'),
		  'first_name': mf('person.first_name'),
		  'last_name': mf('person.last_name'),
		  'date_of_birth': mf('datetime.date'),
		  'address': mf('address.city'),
		  'job_title': mf('person.occupation'),
		  'phone': mf('person.telephone'),
		  'phone_type': mf('choice', items=[1, 2, 3]),
    })
    return {
	    **schema.create(iterations=1)[0], # type: ignore[misc]
	    **{'password1': password, 'password2': password},
	    **fields,
    }