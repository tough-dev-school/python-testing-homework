import pytest
from server.apps.identity.container import container
from server.apps.identity.logic.usecases.user_create_new import UserCreateNew


@pytest.mark.django_db()
def test_create_lead(mock_user_model, mock_user_create_api, assert_correct_user):
    create_lead = container.instantiate(UserCreateNew)
    create_lead(user=mock_user_model)
    assert_correct_user(
        mock_user_model.email,
        {
            'lead_id': mock_user_create_api['id']
        })

