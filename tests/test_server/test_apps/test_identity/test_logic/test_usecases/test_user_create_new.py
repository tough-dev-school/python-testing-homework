import pytest

from server.apps.identity.intrastructure.services.placeholder import UserResponse
from server.apps.identity.logic.usecases.user_create_new import UserCreateNew
from server.apps.identity.models import User
from server.common.django.types import Settings


class TestUserCreateNew:
    @pytest.mark.django_db()
    def test_success_create_new_user(
        self,
        user: User,
        settings: Settings,
        assert_correct_user,
        reg_data,
        expected_user_data,
    ) -> None:
        not_lead_user = User.objects.get(email=reg_data['email'])
        assert not_lead_user.lead_id is None
        assert_correct_user(reg_data['email'], expected_user_data)

        UserCreateNew(settings=settings)(user=user)
        lead_user = User.objects.get(email=reg_data['email'])
        expected_lead_id = 11
        assert lead_user.lead_id == expected_lead_id

    @pytest.mark.django_db()
    def test_success_update_user_ids(
        self,
        user: User,
        settings: Settings,
        assert_correct_user,
        reg_data,
        expected_user_data,
    ) -> None:
        assert_correct_user(reg_data['email'], expected_user_data)
        response = UserResponse(id=100)
        UserCreateNew(settings=settings)._update_user_ids(user=user, response=response)
        actual_user = User.objects.get(email=reg_data['email'])
        assert actual_user.lead_id == response.id
