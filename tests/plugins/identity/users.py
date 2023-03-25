from datetime import datetime
from typing import TypedDict, final

import pytest
from mimesis import Address, Numeric, Person
from mimesis.schema import Field
from typing_extensions import Required

from server.apps.identity.intrastructure.services.placeholder import (
    UserResponse,
)
from server.apps.identity.models import User


class UserData(TypedDict, total=False):
    email: Required[str]
    first_name: str
    last_name: str
    date_of_birth: datetime
    address: str
    job_title: str
    phone: str
    phone_type: int


@final
class RegistrationData(UserData, total=False):
    password1: str
    password2: str


@pytest.fixture()
def user_data(mimesis_seed: int) -> UserData:
    mf = Field(seed=mimesis_seed)
    person = Person(seed=mimesis_seed)
    address = Address(seed=mimesis_seed)
    return UserData(
        email=person.email(),
        first_name=person.first_name(),
        last_name=person.last_name(),
        date_of_birth=mf('datetime.date'),
        address=address.city(),
        job_title=person.occupation(),
        phone=person.telephone(),
        phone_type=mf('choice', items=[1, 2, 3]),
    )


@pytest.fixture()
def registration_data(
    user_data: UserData,
    mimesis_seed: int,
) -> RegistrationData:
    password = Person(seed=mimesis_seed).password()
    return RegistrationData(
        **user_data,
        password1=password,
        password2=password,
    )


@pytest.fixture()
def user_id_response() -> UserResponse:
    return UserResponse(id=Numeric().increment())


@pytest.fixture()
def user(mimesis_seed: int) -> User:
    person = Person(seed=mimesis_seed)
    user = User(email=person.email(), password=person.password())
    user.save()
    return user
