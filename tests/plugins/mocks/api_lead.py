import json
import re
from http import HTTPStatus
from typing import TYPE_CHECKING
from urllib.parse import urljoin

import httpretty
import pytest
from mimesis import Field, Locale

if TYPE_CHECKING:
    from server.common.django.types import Settings


DEFAULT_SEED = 0xFF


@pytest.fixture()
def lead_create_response():
    """Mock LeadResponse on creation."""
    mf = Field(locale=Locale.RU, seed=DEFAULT_SEED)
    return str(mf('numeric.increment'))


@pytest.fixture()
def mock_lead_create(settings: 'Settings', lead_create_response):
    """Mock Lead creation."""
    with httpretty.enabled(allow_net_connect=False):
        httpretty.register_uri(
            httpretty.POST,
            urljoin(
                settings.PLACEHOLDER_API_URL,
                'users',
            ),
            status=HTTPStatus.CREATED,
            body=json.dumps({'id': lead_create_response}),
        )
        yield lead_create_response
        assert httpretty.has_request()


@pytest.fixture()
def mock_lead_update(settings: 'Settings'):
    """Mock Lead update."""
    with httpretty.enabled(allow_net_connect=False):
        httpretty.register_uri(
            httpretty.POST,
            urljoin(
                settings.PLACEHOLDER_API_URL,
                re.compile(r'users/\d+'),
            ),
            status=HTTPStatus.OK,
        )
        yield httpretty.last_request
        assert httpretty.has_request()
