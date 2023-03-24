from typing import TYPE_CHECKING, Final, final

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from server.common.django.models import TimedMixin

# For now, we use a single length for all items, later it can be changed.
_NAME_LENGTH: Final = 254


@final
class _UserManager(BaseUserManager['User']):
    def create_user(
        self,
        email: str,
        password: str,
        **extra_fields,
    ) -> 'User':
        """Create user: regular registration process."""
        if not email:
            # We double-check it here,
            # but validation should make this unreachable.
            raise ValueError('Users must have an email address')

        user = User(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        password: str,
        **extra_fields,
    ) -> 'User':
        """Create superuser."""
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        # Technically this is not transaction safe, but who cares.
        # It is only used in CLI / tests:
        user.save(using=self._db, update_fields=['is_superuser', 'is_staff'])
        return user


@final
class User(AbstractBaseUser, PermissionsMixin, TimedMixin):
    """Implementation of :term:`user` in the app."""

    # Identity:
    email = models.EmailField(unique=True)

    # Details:
    first_name = models.CharField(max_length=_NAME_LENGTH)
    last_name = models.CharField(max_length=_NAME_LENGTH)
    date_of_birth = models.DateField(null=True, blank=False)
    address = models.CharField(max_length=_NAME_LENGTH)
    job_title = models.CharField(max_length=_NAME_LENGTH)

    # Contacts:
    # NOTE: we don't really care about phone correctness.
    phone = models.CharField(max_length=_NAME_LENGTH)

    # Integration with Placeholder API:
    lead_id = models.IntegerField(null=True, blank=True)

    # Security:
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Mechanics:
    objects = _UserManager()  # noqa: WPS110

    USERNAME_FIELD = 'email'  # noqa: WPS115
    USER_DATE_OF_BIRTH_FIELD = 'date_of_birth'  # noqa: WPS115
    REQUIRED_FIELDS = [  # noqa: WPS115
        'first_name',
        'last_name',
        'date_of_birth',
        'address',
        'job_title',
        'phone',
    ]

    if TYPE_CHECKING:  # noqa: WPS604
        # Raw password that is stored in the instance before it is saved,
        # it is actually `str | None` in runtime, but `str` in most tests.
        _password: str
