from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import ListEntry
from crispy_forms.layout import Submit, Reset
from crispy_forms.helper import FormHelper


class ListEntryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ListEntryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('job_submit', _('Add')))
        self.helper.add_input(
            Reset('job_reset', _('Reset'), css_class='btn-default'))

    class Meta:
        model = ListEntry
        exclude = ('user', 'game', )
