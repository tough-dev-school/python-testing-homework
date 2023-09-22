import pytest
from django.http import HttpResponse
from django.shortcuts import render
from django.test import RequestFactory

pytestmark = [
    pytest.mark.django_db,
]


def test_base():
    """Test base template."""
    page = render(RequestFactory().get('/'), 'common/_base.html')

    assert isinstance(page, HttpResponse)


def test_messages():
    """Test messages template."""
    page = render(RequestFactory().get('/'), 'common/includes/messages.html', {
        'messages': ['First', 'second'],
    })

    assert isinstance(page, HttpResponse)
