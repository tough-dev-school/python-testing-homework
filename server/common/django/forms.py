from django import forms


class DateWidget(forms.DateInput):
    """Date input in the proper date format."""

    input_type = 'date'
    format = '%Y-%m-%d'  # noqa: WPS323
