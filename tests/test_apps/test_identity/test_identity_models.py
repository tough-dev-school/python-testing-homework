import pytest


@pytest.mark.django_db
def test_user_model(
        create_user,
        assert_user,
        user_model_data) -> None:
    user = create_user
    assert_user(email=user.email, expected=user_model_data)


@pytest.mark.django_db
def test_super_user(
        create_superuser,
        assert_user) -> None:
    user = create_superuser
    assert_user(email=user.email, superuser=True)
