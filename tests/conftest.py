"""
This module is used to provide configuration, fixtures, and plugins for pytest.

It may be also used for extending doctest's context:
1. https://docs.python.org/3/library/doctest.html
2. https://docs.pytest.org/en/latest/doctest.html
"""
import random
from typing_extensions import TYPE_CHECKING, Unpack

import pytest
from mimesis.locales import Locale
from mimesis.schema import Field, Schema

from server.apps.identity.models import User

if TYPE_CHECKING:
    from plugins.identity.user import (
        RegisteredData,
        RegistrationData,
        RegistrationDataFactory,
        UserData,
    )

pytest_plugins = [
    # Should be the first custom one:
    'plugins.django_settings',

    # TODO: add your own plugins here!
]

@pytest.fixture(scope="session")
def faker_seed():
    return random.Random().getrandbits(32)


@pytest.fixture()
def registration_data_factory(
    faker_seed: int,
) -> "RegistrationDataFactory":
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
            },
        )
        return {
            **schema.create(iterations=1)[0],  # type: ignore[misc]
            **{"password1": password, "password2": password},
            **fields,
        }

    return factory


@pytest.fixture()
def registration_data(
    registration_data_factory: "RegistrationDataFactory",
) -> "RegistrationData":
    return registration_data_factory()


@pytest.fixture()
def user_data(registration_data: "RegistrationData") -> "UserData":
    return {  # type: ignore [return-value]
        key_name: value_part
        for key_name, value_part in registration_data.items()
        if not key_name.startswith("password")
    }

@pytest.fixture()
def expected_user_data(user_data: "RegistrationData"):
    return user_data

@pytest.fixture()
def registered_data(registration_data: "RegistrationData") -> "RegisteredData":
    return { # type: ignore [return-value]
        ('password' if key_name.startswith("password") else key_name): value_part
        for key_name, value_part in registration_data.items()
    }

@pytest.fixture()
def register_user(registered_data: "RegisteredData") -> dict[str, str]:
    User.objects.create_user(**registered_data)
    return { #type: ignore
        'username': registered_data["email"],
        'password': registered_data["password"]
    }