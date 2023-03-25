
# import pytest
# from server.apps.identity.models import User

# from django.test import Client
# from http import HTTPStatus
# from django.urls import reverse


# @pytest.mark.django_db()
# def test_update_user(registered_user: User):

#     response = client.post(
#         reverse("identity:user_update"),
#         data={'username': registered_user['email'], 'password': registered_user['password']}
#     )

#     assert response.status_code == HTTPStatus.OK



# @pytest.mark.django_db()
# def test_create_user_with_valid_data(
#     client: Client,
#     registration_data: "RegistrationData",
#     expected_user_data: "UserData",
#     assert_correct_user: "UserAssertion",
# ) -> None:
#     response = client.post(
#         reverse("identity:registration"),
#         data=registration_data,
#     )

#     assert response.status_code == HTTPStatus.FOUND
#     assert response.get("location") == reverse("identity:login")
#     assert_correct_user(registration_data["email"], expected_user_data)
