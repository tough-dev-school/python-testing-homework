from typing import Generator

import pytest
from django.conf import settings

from tests.plugins.constants import URL_JSON_SERVER_FINAL


@pytest.fixture()
def _apply_json_server() -> Generator[None, None, None]:
    """Mock DJANGO_PLACEHOLDER_API_URL using json_server."""
    previous_setting = settings.PLACEHOLDER_API_URL  # type: ignore[misc]
    settings.PLACEHOLDER_API_URL = URL_JSON_SERVER_FINAL

    yield

    settings.PLACEHOLDER_API_URL = previous_setting
