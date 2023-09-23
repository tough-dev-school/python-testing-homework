from typing import final

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import UpdateView
from ratelimit.mixins import RatelimitMixin

from server.apps.identity.container import container
from server.apps.identity.infrastructure.django.forms import UserUpdateForm
from server.apps.identity.logic.usecases.user_update import UserUpdate
from server.apps.identity.models import User
from server.common.django.decorators import dispatch_decorator


@final
@dispatch_decorator(login_required)
@dispatch_decorator(sensitive_post_parameters('email'))
class UserUpdateView(RatelimitMixin, UpdateView[User, UserUpdateForm]):
    """Change user details."""

    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('identity:user_update')
    template_name = 'identity/pages/user_update.html'

    # Rate-limiting:
    ratelimit_key = 'ip'
    ratelimit_rate = '10/h'
    ratelimit_block = True
    ratelimit_method = ['POST', 'PUT']  # GET is safe

    def get_object(self, queryset: QuerySet[User] | None = None) -> User:
        """We only work with the current user."""
        assert self.request.user.is_authenticated  # more for mypy  # noqa: S101
        return self.request.user

    def form_valid(self, form: UserUpdateForm) -> HttpResponse:
        """
        Data is valid.

        In this case we need to:
        1. Show success message
        2. Sync information with :term:`Placeholder API`
        """
        user_update = container.instantiate(UserUpdate)

        # Using Russian text without `gettext` is ugly, but we don't support
        # other languages at all in this demo.
        messages.success(self.request, 'Ваши данные сохранены')
        response = super().form_valid(form)
        user_update(self.object)
        return response
