import pytest

from server.apps.identity.intrastructure.services.placeholder import LeadUpdate, LeadCreate
from server.apps.identity.models import User
from server.common.django.types import Settings


@pytest.mark.django_db()
def test_lead_update(settings: Settings, mock_user_model: User, mock_user_update_api):
    """Test LeadUpdate service calls remote user API and returns id"""
    lead_update_service = LeadUpdate(settings.PLACEHOLDER_API_URL, settings.PLACEHOLDER_API_TIMEOUT)
    lead_update_service(user=mock_user_model)


@pytest.mark.django_db()
def test_lead_create(settings: Settings, mock_user_model: User, mock_user_create_api):
    """Test LeadCreate service calls remote user API"""
    lead_create_service = LeadCreate(settings.PLACEHOLDER_API_URL, settings.PLACEHOLDER_API_TIMEOUT)
    user_response = lead_create_service(user=mock_user_model)
    assert user_response.id == mock_user_create_api['id']
