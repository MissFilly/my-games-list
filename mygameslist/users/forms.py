from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django_summernote.widgets import SummernoteInplaceWidget
from .models import UserProfile


class SignupForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, label=_('First name'))
    last_name = forms.CharField(max_length=30, label=_('Last name'))

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'gender', 'country']

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        profile = user.profile
        profile.gender = self.cleaned_data['gender']
        profile.country = self.cleaned_data['country']
        profile.save()
        user.save()


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        widgets = {
            'about': SummernoteInplaceWidget(),
        }
        exclude = ('user', )

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Save')))
