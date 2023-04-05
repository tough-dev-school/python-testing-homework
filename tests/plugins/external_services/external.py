import pytest
import requests

JSON_SERVER_BASE_URL = "json-server-container:3000"


@pytest.fixture()
def json_server_get_picture():
    return requests.get(
        f"http://{JSON_SERVER_BASE_URL}/pictures", timeout=(2, 3)
    ).json()
