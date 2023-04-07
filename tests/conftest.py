"""
This module is used to provide configuration, fixtures, and plugins for pytest.

It may be also used for extending doctest's context:
1. https://docs.python.org/3/library/doctest.html
2. https://docs.pytest.org/en/latest/doctest.html
"""

import pytest

pytest_plugins = [
    # Should be the first custom one:
    'plugins.django_settings',

    # TODO: add your own plugins here!
]



@pytest.fixture(scope='session')
def user(request) -> str:
	return 'kadochnikovs'



@pytest.fixture(scope='function')
def user_id(request) -> str:


@pytest.fixture(params=[
	1,
	2,
])
def user_id(request) -> int:
	return request.param

@pytest.fixture(params=[
	'',
	'ololo',
    'ololo'*100

])
def user_name(request) -> int:
	return request.param
