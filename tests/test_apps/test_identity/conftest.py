# import datetime as dt
# import random
# from typing import final, TypedDict, Optional, TypeAlias, Callable
#
# import pytest
# from django.test import Client
# from mimesis import Field, Locale, Schema
#
# from server.apps.identity.models import User
#
#
# @final
# class RegistrationData(TypedDict, total=False):
#     """Represent the user data that is required to create a new user."""
#
#     email: str
#     first_name: str
#     last_name: str
#     date_of_birth: dt.datetime
#     address: str
#     job_title: str
#     phone: str
#     phone_type: int
#     password: str
#     password1: Optional[str]
#     password2: Optional[str]
#
#
# @final
# class LoginData(TypedDict, total=False):
#     """Represent the user data that is required to login."""
#
#     email: str
#     password: str
#
#
# UserAssertion: TypeAlias = Callable[[RegistrationData], None]
#
#
# @pytest.fixture()
# def user_factory():
#     """Generate registration data."""
#
#     def factory(**fields) -> RegistrationData:
#         field = Field(locale=Locale.EN, seed=random.randint(1, 1000))
#         password = field('password')  # by default passwords are equal
#         schema = Schema(schema=lambda: {
#             'email': field('person.email'),
#             'first_name': field('person.first_name'),
#             'last_name': field('person.last_name'),
#             'date_of_birth': field('datetime.date'),
#             'address': field('address.city'),
#             'job_title': field('person.occupation'),
#             'phone': field('person.telephone'),
#         },
#                         iterations=1)
#         return {
#             **schema.create()[0],  # type: ignore[misc]
#             **{'password': password},
#             **fields,
#         }
#
#     return factory
#
#
# @pytest.fixture()
# def user_data(user_factory):
#     """Random user data from factory."""
#     return user_factory()
#
#
# @pytest.fixture(scope='session')
# def assert_correct_user() -> UserAssertion:
#     """Check that user created correctly."""
#
#     def factory(expected: RegistrationData) -> None:
#         user = User.objects.get(email=expected['email'])
#         # Special fields:
#         assert user.id
#         assert user.is_active
#         assert not user.is_superuser
#         assert not user.is_staff
#         # All other fields:
#         for field_name, data_value in expected.items():
#             if not field_name.startswith('password'):
#                 assert getattr(user, field_name) == data_value
#
#     return factory
#
#
# @pytest.fixture()
# def registration_data(user_data: RegistrationData) -> RegistrationData:
#     """User data."""
#     user_data['password1'] = user_data['password']
#     user_data['password2'] = user_data['password']
#
#     return user_data
#
#
# @pytest.mark.django_db()
# @pytest.fixture()
# def create_new_user(user_data: RegistrationData) -> User:
#     """Create new user."""
#     user = User.objects.create_user(**user_data)
#     user.set_password(user_data['password'])
#     user.save()
#     return user
#
#
# @pytest.mark.django_db()
# @pytest.fixture()
# def create_new_user(user_data: RegistrationData) -> User:
#     """Create new user."""
#     user = User(**user_data)
#     user.set_password(user_data['password'])
#     user.save()
#
#     return user
#
# @pytest.fixture()
# def login_data(user_data: RegistrationData) -> LoginData:
#     """Login data from``registration_data``."""
#     return {
#         'username': user_data['email'],
#         'password': user_data['password'],
#     }
#
#
# @pytest.mark.django_db()
# @pytest.fixture()
# def login(client: Client, create_new_user: User) -> User:
#     """Login as valid user."""
#     client.force_login(create_new_user)
#
#     return create_new_user
