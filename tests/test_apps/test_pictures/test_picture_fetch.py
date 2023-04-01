from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db()
def test_dashboard_loads(logged_client: Client):

    response = logged_client.get(reverse("pictures:dashboard"))

    assert response.status_code == HTTPStatus.OK
