from server.apps.identity.models import User


def assert_correct_user(user_email, expected_data):
    user = User.objects.get(email=user_email)
    assert user.id
    assert user.is_active
    assert not user.is_superuser
    assert not user.is_staff
    for field_name, data_value in expected_data.items():
        assert getattr(user, field_name) == data_value
