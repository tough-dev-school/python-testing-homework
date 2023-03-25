"""
This module is used to provide configuration, fixtures, and plugins for pytest.

It may be also used for extending doctest's context:
1. https://docs.python.org/3/library/doctest.html
2. https://docs.pytest.org/en/latest/doctest.html
"""

pytest_plugins = [
    # Should be the first custom one:
    'tests.plugins.django_settings',
    'tests.plugins.identity.user',
    'tests.plugins.common.admin_client_app',

    # TODO: add your own plugins here!
]
