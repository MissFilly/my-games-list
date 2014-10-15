from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.layout import Submit
from crispy_forms.helper import FormHelper


class FriendRequestForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(),
                              initial=_('Hi, I would like to add you to my '
                                        'friends list.'))

    def __init__(self, *args, **kwargs):
        super(FriendRequestForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Send')))
