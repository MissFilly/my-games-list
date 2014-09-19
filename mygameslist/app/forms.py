from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import ListEntry, Game, GameReview, GameRecommendation
from crispy_forms.layout import Submit, Reset
from crispy_forms.helper import FormHelper


class ListEntryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ListEntryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Add')))
        self.helper.add_input(
            Reset('job_reset', _('Reset'), css_class='btn-default'))

    class Meta:
        model = ListEntry
        exclude = ('user', 'game', )


class ListEntryChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return obj.game


class GameReviewForm(forms.ModelForm):
    entry = ListEntryChoiceField(queryset=ListEntry.objects.none(),
                                 label=_('Game'))

    def __init__(self, user=None, *args, **kwargs):
        super(GameReviewForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['entry'].queryset = ListEntry.objects.filter(user=user)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Submit')))

    class Meta:
        model = GameReview
        exclude = ('user',)
