from django import forms
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from .models import *
from crispy_forms.layout import Submit, Reset, Layout
from crispy_forms.helper import FormHelper

from django_summernote.widgets import SummernoteInplaceWidget


class ListEntryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ListEntryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Save')))
        self.helper.add_input(
            Reset('job_reset', _('Reset'), css_class='btn-default'))

    class Meta:
        model = ListEntry
        fields = ('status', 'score', 'replay_value')


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
        return obj.game_title


class GameRecommendationForm(forms.ModelForm):
    similar = ListEntryChoiceField(queryset=ListEntry.objects.none(),
                                   label=_('Similar recommendation'))

    def __init__(self, user, entry, *args, **kwargs):
        super(GameRecommendationForm, self).__init__(*args, **kwargs)
        similar = self.fields['similar']
        # Exclude entries that already have a recommendation for this
        # game, and the entry for this game too
        similar.queryset = ListEntry.objects.filter(user=user) \
            .exclude(Q(recommendation_entry1__entry1=entry) | \
                     Q(recommendation_entry1__entry2=entry) |
                     Q(recommendation_entry2__entry1=entry) |
                     Q(recommendation_entry2__entry2=entry)) \
            .exclude(pk=entry.pk)
        self.entry = entry
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Submit')))

    class Meta:
        model = GameRecommendation
        fields = ['similar', 'text', ]


class GameRecommendationEditForm(forms.ModelForm):

    class Meta:
        model = GameRecommendation
        fields = ['text', ]

    def __init__(self, *args, **kwargs):
        super(GameRecommendationEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Submit')))


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
