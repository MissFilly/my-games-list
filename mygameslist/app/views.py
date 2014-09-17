from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic.detail import DetailView
from .models import Game, GameReview, GameRecommendation, \
    UserProfile


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
        context['reviews'] = GameReview.objects.filter(game=self.object)
        context['recommendations'] = GameRecommendation.objects.filter(
            Q(game1=self.object) | Q(game2=self.object))
        return context
