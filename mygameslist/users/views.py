from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404

from social.apps.django_app.default.models import UserSocialAuth

from mygameslist.mixins import LoginRequiredMixin
from mygameslist.app.models import GameReview, GameRecommendation
from .models import User, UserProfile
from .forms import UserProfileForm


class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    slug_field = 'username'

    def get_context_data(self, section=None, *args, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        reviews = GameReview.objects_with_scores.filter(entry__user=self.object).order_by('-date_created')
        recommendations = GameRecommendation.objects_with_scores.filter(entry1__user=self.object) \
                                                                .distinct().order_by('-date_created')
        section = self.kwargs.get('section')
        if section == 'reviews':
            context['reviews_page'] = True
        elif section == 'recommendations':
            context['recommendations_page'] = True
        else:
            context['detail_page'] = True
            reviews = reviews[:3]
            recommendations = recommendations[:3]
        context['reviews'] = reviews
        context['recommendations'] = recommendations
        return context


class UserReviewsView(ListView):
    model = GameReview
    template_name = 'user_detail.html'

    def get_queryset(self):
        self.user_profile = get_object_or_404(User, username=self.kwargs.get('slug'))
        return self.model.objects.filter(entry__user=self.user_profile)

    def get_context_data(self, **kwargs):
        context = super(UserReviewsView, self).get_context_data(**kwargs)
        context['object'] = self.user_profile
        context['reviews'] = self.object_list
        context['reviews_page'] = True
        return context


class UserRecommendationsView(ListView):
    model = GameRecommendation
    template_name = 'user_detail.html'

    def get_queryset(self):
        self.user_profile = get_object_or_404(User, username=self.kwargs.get('slug'))
        return self.model.objects_with_scores.filter(entry1__user=self.user_profile).distinct()

    def get_context_data(self, **kwargs):
        context = super(UserRecommendationsView, self).get_context_data(**kwargs)
        context['object'] = self.user_profile
        context['recommendations'] = self.object_list
        context['recommendations_page'] = True
        return context


class UserProfileUpdate(LoginRequiredMixin, UpdateView):

    model = UserProfile
    form_class = UserProfileForm
    template_name = 'app/userprofile_form.html'

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super(UserProfileUpdate, self).get_context_data(**kwargs)
        steam_account_exists = UserSocialAuth.objects.filter(
            provider='steam',
            user=self.request.user).exists()
        context['steam_account_exists'] = steam_account_exists
        return context
