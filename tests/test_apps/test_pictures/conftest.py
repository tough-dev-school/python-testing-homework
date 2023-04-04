from http import HTTPStatus

import pytest
from django.urls import reverse
from mimesis.schema import Field, Schema


@pytest.fixture()
def picture_data_factory():
    def factory(**fields):
        mf = Field()
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
