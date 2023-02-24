from django.db import models


class TimedMixin(models.Model):
    """Adding utility time fields for different models."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(object):
        abstract = True
