import pytest

from server.apps.identity.container import container
from server.apps.identity.logic.usecases.user_update import UserUpdate


@pytest.mark.django_db()
def test_lead_update(mock_user_model, mock_user_update_api):
    """Test UserUpdate use case calls remote service to update user data"""
    create_lead = container.instantiate(UserUpdate)
    create_lead(user=mock_user_model)

