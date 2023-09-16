from http import HTTPStatus
import re
from typing import TYPE_CHECKING
from urllib.parse import urljoin
import pytest

from server.apps.identity.models import User

import httpretty
from mimesis import Field, Locale

if TYPE_CHECKING:
    from server.common.django.types import Settings


@pytest.fixture()
def lead_create_response():
    mf = Field(locale=Locale.RU, seed=0xFF)
    return str(mf('numeric.increment'))


@pytest.fixture()
def mock_lead_create(settings: 'Settings', lead_create_response):
    with httpretty.enabled(allow_net_connect=False):
        httpretty.register_uri(
            httpretty.POST,
            urljoin(
                settings.PLACEHOLDER_API_URL,
                'users',
            ),
            status=HTTPStatus.CREATED,
            body=lead_create_response,
        )
        yield lead_create_response
        assert httpretty.has_request()


@pytest.fixture()
def mock_lead_update(settings: 'Settings'):
    with httpretty.enabled(allow_net_connect=False):
        httpretty.register_uri(
            httpretty.POST,
            urljoin(
                settings.PLACEHOLDER_API_URL,
                re.compile('users/\d+'),
            ),
            status=HTTPStatus.OK,
        )
        yield
        assert httpretty.has_request()
