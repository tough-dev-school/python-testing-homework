import pytest


@pytest.fixture(scope='function')
def username(request) -> str:
	return 'sobolevn'


def load_user(username: str):
    if username:
        return username
    else:
        return None

def test_user_id(username: str) -> None:
	# значение username, которое создали в фикстуре, попадёт в эту тестирующую функцию
	assert load_user(username) is not None
