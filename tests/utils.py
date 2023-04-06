from contextlib import contextmanager
from typing import Iterator

import httpretty
from django.conf import settings
from pydantic import BaseModel


@contextmanager
def mock_external_endpoint(
    method: str,
    endpoint: str,
    response_body: BaseModel,
) -> Iterator[None]:
    with httpretty.enabled():
        httpretty.register_uri(
            method=method,
            body=response_body.json(),
            uri=settings.PLACEHOLDER_API_URL + endpoint,
        )
        yield
        assert httpretty.has_request()
        httpretty.reset()
