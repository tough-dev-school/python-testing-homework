import pytest
from django.test import Client, RequestFactory
from django.urls import reverse

from server.apps.identity.models import User
from server.apps.pictures.views import DashboardView

pytestmark = [pytest.mark.django_db]

url = reverse('pictures:dashboard')


def test_pictures_in_context_data(authorized_client: Client):
    response = authorized_client.get(url)
    assert "pictures" in response.context


def test_user_in_form_kwargs(user: User, request_factory: RequestFactory):
    request = request_factory.get(url)
    request.user = user

    view = DashboardView()
    view.setup(request)
    form_kwargs = view.get_form_kwargs()

    assert "user" in form_kwargs


@pytest.mark.timeout(5)
@pytest.mark.usefixtures("json_server_on")
def test_external_service(authorized_client):
    response = authorized_client.get(url)
    response_pictures = response.context["pictures"]
    assert response_pictures
