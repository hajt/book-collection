from django import forms
from urllib.parse import urlparse
from django.core.exceptions import ValidationError
from typing import Optional


def validate_googleapis_hostname(url: str) -> Optional[ValidationError]:
    """ Method for validation is hostname belongs to Google APIs. """
    url = urlparse(url)
    if url.hostname not in ['googleapis.com', 'www.googleapis.com']:
        raise ValidationError('Only Google APIs URL allowed')


class ApiImportForm(forms.Form):
    """ Form for passing External API URL. """
    url = forms.URLField(label='External API URL', required=True, validators=[validate_googleapis_hostname])
