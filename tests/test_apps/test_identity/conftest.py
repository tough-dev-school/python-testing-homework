import random
import datetime as dt

import pytest
from mimesis.locales import Locale
from mimesis.schema import Field, Schema
from django.urls import reverse


@pytest.fixture(scope="session")
def faker_seed():
    return random.randint(1, 10)


@pytest.fixture()
def registration_data_factory(faker_seed):
    def factory(**fields):
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
def registration_data(registration_data_factory):
    return registration_data_factory()


@pytest.fixture()
def user_data(registration_data):
    return {
        key_name: value_part
        for key_name, value_part in registration_data.items()
        if not key_name.startswith("password")
    }


@pytest.fixture()
def register_user_factory(client, registration_data_factory):
    def factory():
        user_data = registration_data_factory()
        client.post(reverse("identity:registration"), data=user_data)
        return (user_data["email"], user_data["password1"])

    return factory


@pytest.fixture()
def signup_user(client, register_user_factory):
    user_email, password = register_user_factory()
    client.post(
        reverse("identity:login"), data={"username": user_email, "password": password}
    )
    return {"email": user_email, "password": password}
