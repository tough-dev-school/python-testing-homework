from typing import final

from axes.decorators import axes_dispatch
from django.contrib.auth.views import LoginView as BaseLoginView
from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.edit import FormView
from ratelimit.mixins import RatelimitMixin

from server.apps.identity.container import container
from server.apps.identity.infrastructure.django.decorators import (
    redirect_logged_in_users,
)
from server.apps.identity.infrastructure.django.forms import (
    AuthenticationForm,
    RegistrationForm,
)
from server.apps.identity.logic.usecases.user_create_new import UserCreateNew
from server.common.django.decorators import dispatch_decorator


@final
@dispatch_decorator(redirect_logged_in_users())
@dispatch_decorator(axes_dispatch)
@dispatch_decorator(sensitive_post_parameters())
class LoginView(BaseLoginView):
    """More protected version of the login view."""

    form_class = AuthenticationForm


@final
@dispatch_decorator(redirect_logged_in_users())
@dispatch_decorator(sensitive_post_parameters())
class RegistrationView(RatelimitMixin, FormView[RegistrationForm]):
    """
    Registers users.

    After the registration we notify :term:`Placeholder API`
    about new users and get their ids back.
    """

    form_class = RegistrationForm
    template_name = 'identity/pages/registration.html'
    success_url = reverse_lazy('identity:login')

    # Rate-limiting:
    ratelimit_key = 'ip'
    ratelimit_rate = '5/h'
    ratelimit_block = True
    ratelimit_method = ['POST', 'PUT']  # GET is safe

    def form_valid(self, form: RegistrationForm) -> HttpResponse:
        """Save user after successful validation."""
        user_create_new = container.instantiate(UserCreateNew)
        with transaction.atomic():
            user = form.save()
            user_create_new(user)  # does http request, can slow down db
        return super().form_valid(form)
