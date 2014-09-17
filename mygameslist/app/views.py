from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Game, GameReview, GameRecommendation, \
    UserProfile, ListEntry


def home(request):
    reviews = GameReview.objects.order_by('-date_created')[:6]
    recommendations = GameRecommendation.objects.order_by('-date_created')[:6]
    context = dict(reviews=reviews, recommendations=recommendations)
    return render(request, 'index.html', context)


class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    slug_field = 'username'


class GameDetailView(DetailView):
    model = Game
    template_name = 'game_detail.html'

    def get_context_data(self, **kwargs):
        context = super(GameDetailView, self).get_context_data(**kwargs)
        game = self.object
        context['reviews'] = GameReview.objects.filter(game=game)
        context['recommendations'] = GameRecommendation.objects.filter(
            Q(game1=game) | Q(game2=game))

        user = self.request.user
        if user.is_authenticated():
            context['object_in_user_list'] = ListEntry.objects.filter(
                user=user,
                game=self.object
            ).exists()
        return context


class GameListByUserView(ListView):
    model = ListEntry
    template_name = 'game_list_by_user.html'

    def get_queryset(self):
        self.user_profile = get_object_or_404(User, username=self.kwargs['slug'])
        return ListEntry.objects.filter(user=self.user_profile)

    def get_context_data(self, **kwargs):
        context = super(GameListByUserView, self).get_context_data(**kwargs)
        context['user_profile'] = self.user_profile
        return context
