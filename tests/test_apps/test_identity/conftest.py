import random
from typing import Callable, Dict, Protocol, final
from django.test import Client

import pytest
from typing_extensions import Unpack, TypeAlias
from mimesis.locales import Locale
from mimesis.schema import Field, Schema
from django.urls import reverse


CreateUserFactory: TypeAlias = Callable[[], Dict[str, str]]


@final
class RegistrationDataFactory(Protocol):
    def __call__(
        self,
        **fields: Unpack["RegistrationData"],
    ) -> "RegistrationData":
        pass


@pytest.fixture(scope="session")
def faker_seed() -> int:
    return random.Random().getrandbits(32)


@pytest.fixture()
def registration_data_factory(faker_seed: int) -> RegistrationDataFactory:
    def factory(**fields: Unpack["RegistrationData"]) -> "RegistrationData":
        mf = Field(locale=Locale.RU, seed=faker_seed)
        password = mf("password")
        schema = Schema(
            schema=lambda: {
                "email": mf("person.email"),
                "first_name": mf("person.first_name"),
                "last_name": mf("person.last_name"),
                "date_of_birth": mf("datetime.date"),
                "address": mf("address.city"),
                "job_title": mf("person.occupation"),
                "phone": mf("person.telephone"),
            }
        )
        return {
            **schema.create(iterations=1)[0],
            **{"password1": password, "password2": password},
            **fields,
        }

    return factory


@pytest.fixture()
def registration_data(
    registration_data_factory: RegistrationDataFactory,
) -> "RegistrationData":
    return registration_data_factory()


@pytest.fixture()
def user_data(registration_data: "RegistrationData") -> "UserData":
    return {
        key_name: value_part
        for key_name, value_part in registration_data.items()
        if not key_name.startswith("password")
    }


@pytest.fixture()
def create_new_user_factory(
    client: Client, registration_data_factory: RegistrationDataFactory
) -> CreateUserFactory:
    def factory() -> Dict[str, str]:
        user_data = registration_data_factory()
        client.post(reverse("identity:registration"), data=user_data)
        return {"email": user_data["email"], "password": user_data["password1"]}

    return factory


@pytest.fixture()
def signup_user(
    client: Client, create_new_user_factory: CreateUserFactory
) -> Dict[str, str]:
    user_info = create_new_user_factory()
    client.post(
        reverse("identity:login"),
        data={"username": user_info["email"], "password": user_info["password"]},
    )
    return user_info
