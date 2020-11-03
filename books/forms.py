from django import forms


class ApiImportForm(forms.Form):
    """ Form for passing External API URL. """
    url = forms.URLField(label='External API URL', required=True)
