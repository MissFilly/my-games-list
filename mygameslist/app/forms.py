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

    def __init__(self, *args, **kwargs):
        super(GameReviewForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Submit')))

    class Meta:
        model = GameReview
        exclude = ('entry', )


class ListEntryChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return obj.game


class GameRecommendationForm(forms.ModelForm):
    similar = ListEntryChoiceField(queryset=ListEntry.objects.none(),
                                   label=_('Similar recommendation'))

    def __init__(self, user, entry, *args, **kwargs):
        super(GameRecommendationForm, self).__init__(*args, **kwargs)
        similar = self.fields['similar']
        # Exclude entry for which the recommendation is being made
        similar.queryset = ListEntry.objects.filter(
            user=user).exclude(gamerecommendation__entries=entry)
        self.entry = entry
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Submit')))

    class Meta:
        model = GameRecommendation
        fields = ['similar', 'text', ]

    def clean(self):
        cleaned_data = super(GameRecommendationForm, self).clean()
        similar = cleaned_data.get('similar')

        if self.entry and similar:
            query = GameRecommendation.objects.filter(
                entries__pk=self.entry.pk)
            query = GameRecommendation.objects.filter(entries__pk=similar.pk)
            if query.exists():
                raise forms.ValidationError(
                    _("You have already recommended this game."))
        return cleaned_data


class GameRecommendationEditForm(forms.ModelForm):

    class Meta:
        model = GameRecommendation
        fields = ['text', ]

    def __init__(self, *args, **kwargs):
        super(GameRecommendationEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Submit')))
