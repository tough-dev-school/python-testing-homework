from typing import Any, Callable, TypeVar

from django.utils.decorators import method_decorator

_Type = TypeVar('_Type', bound=type)


def dispatch_decorator(func: Callable[..., Any]) -> Callable[[_Type], _Type]:
    """Special helper to decorate class-based view's `dispatch` method."""
    return method_decorator(func, name='dispatch')
