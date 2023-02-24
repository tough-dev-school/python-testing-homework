from typing import Any


class TimeReadOnlyMixin(object):
    """Utility class to represent readonly dates in the admin panel."""

    readonly_fields: Any = ('created_at', 'updated_at')
