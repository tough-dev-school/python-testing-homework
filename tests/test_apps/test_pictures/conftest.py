import random
from http import HTTPStatus

import pytest
import requests
from django.urls import reverse
from mimesis.schema import Field, Schema


@pytest.fixture()
def picture_data_factory(faker_seed):
    def factory(**fields):
        mf = Field(seed=faker_seed)
        schema = Schema(
            schema=lambda: {
                "foreign_id": mf("numeric.increment"),
                "url": mf("internet.url"),
            }
        )
        return {
            **schema.create(iterations=1)[0],
            **fields,
        }

    return factory


@pytest.fixture()
def get_picture_data(picture_data_factory):
    return picture_data_factory()


@pytest.fixture()
def add_favourite_picture(client):
    def factory(picture_data):
        response = client.post(reverse("pictures:dashboard"), data=picture_data)
        assert response.status_code == HTTPStatus.FOUND

    return factory


@pytest.fixture(params=["internal", "json-server", "external"])
def valid_new_picture(request, picture_data_factory, json_server_get_picture):
    if request.param == "internal":
        return picture_data_factory()
    elif request.param == "json-server":
        picture = random.choice(json_server_get_picture)
        return {"foreign_id": picture["id"], "url": picture["url"]}
    else:
        response = requests.get("https://api.scryfall.com/cards/random")
        picture = response.json()
        picture = (
            picture if not picture.get("card_faces") else picture["card_faces"]
        )
        picture = {
            "foreign_id": random.randint(100, 1000),
            "url": response.json()["image_uris"]["normal"],
        }
        return picture
