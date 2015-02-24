from django import forms
from django.utils.translation import ugettext as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Fieldset, Layout, ButtonHolder, Div
from mygameslist.app.models import Platform, Genre


class PlatformForm(forms.Form):
    platform = forms.ModelChoiceField(queryset=Platform.objects.all(), required=False)
    genre = forms.ModelChoiceField(queryset=Genre.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(PlatformForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                'platform',
                css_class='col-md-5'
            ),
            Div(
                'genre',
                css_class='col-md-5'
            ),
            ButtonHolder(
                Submit('submit', _('Filter')),
                css_class='col-md-2'
            )
        )
