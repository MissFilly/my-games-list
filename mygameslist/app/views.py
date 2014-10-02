from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.http import Http404
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from gamesdb.api import API

from .models import *
from .forms import *
from .mixins import *

gamesdb_api = API()


def home(request):
    reviews = GameReview.objects.order_by('-date_created')[:4]
    recommendations = GameRecommendation.objects.order_by('-date_created')[:4]
    context = dict(reviews=reviews, recommendations=recommendations)
    return render(request, 'index.html', context)


class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    slug_field = 'username'

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        user = self.object
        context['reviews'] = GameReview.objects.filter(
            entry__user=user).order_by('-date_created')[:3]
        context['recommendations'] = GameRecommendation.objects.filter(
            entry1__user=user).distinct().order_by('-date_created')[:3]
        context['detail_page'] = True
        return context


class GameDetailView(TemplateView):
    # model = Game
    template_name = 'game_detail.html'

    def get_context_data(self, **kwargs):
        context = super(GameDetailView, self).get_context_data(**kwargs)
        game = gamesdb_api.get_game(id=kwargs['pk'])
        if game is None:
            raise Http404
        reviews = GameReview.objects.filter(
            entry__game_id=game.id).order_by('-date_created')[:3]
        recommendations = GameRecommendation.objects.filter(
            Q(entry1__game_id=game.id) | Q(entry2__game_id=game.id)) \
            .distinct().order_by('-date_created')[:3]

        context = dict(game=game, reviews=reviews,
                       recommendations=recommendations, detail_page=True)
        user = self.request.user
        if user.is_authenticated():
            try:
                context['entry'] = ListEntry.objects.get(user=user,
                                                         game_id=kwargs['pk'])
            except:
                pass
        return context


class GameListByUserView(ListView):
    model = ListEntry
    template_name = 'game_list_by_user.html'

    def get_queryset(self):
        self.user_profile = get_object_or_404(
            User, username=self.kwargs['slug'])
        return ListEntry.objects.filter(user=self.user_profile) \
            .order_by('status')

    def get_context_data(self, **kwargs):
        context = super(GameListByUserView, self).get_context_data(**kwargs)
        context['user_profile'] = self.user_profile
        return context


class ListEntryCreate(LoginRequiredMixin, CreateView):
    model = ListEntry
    form_class = ListEntryForm

    def dispatch(self, request, *args, **kwargs):
        self.game = gamesdb_api.get_game(id=kwargs['pk'])
        if self.game is None:
            raise Http404
        if request.user.is_authenticated():
            entry = ListEntry.objects.filter(user=request.user,
                                             game_id=self.game.id)
            if entry.exists():
                return redirect(reverse(
                    'entry_update',
                    kwargs={'pk': entry.pk, }))
        return super(ListEntryCreate, self).dispatch(request,
                                                     *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.game_id = self.game.id
        form.instance.game_title = self.game.title
        form.instance.game_thumb_url = self.game.thumb_url
        return super(ListEntryCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('game_list_by_user',
                       kwargs={'slug': self.request.user.username, })

    def get_context_data(self, **kwargs):
        context = super(ListEntryCreate, self).get_context_data(**kwargs)
        context['game'] = self.game
        return context


class ListEntryUpdate(PermissionMixin, UpdateView):
    model = ListEntry
    form_class = ListEntryForm

    def get_success_url(self):
        return reverse('game_list_by_user',
                       kwargs={'slug': self.request.user.username, })


class ListEntryDelete(PermissionMixin, DeleteView):
    model = ListEntry

    def get_success_url(self):
        return reverse('game_list_by_user',
                       kwargs={'slug': self.request.user.username, })


class GameReviewCreate(EntryMixin, CreateView):
    model = GameReview
    form_class = GameReviewForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            try:
                review = GameReview.objects.get(entry__game_id=kwargs['pk'],
                                                entry__user=request.user)
                return redirect(reverse('review_update',
                                        kwargs={'pk': review.pk}))
            except GameReview.DoesNotExist:
                self.game = gamesdb_api.get_game(id=kwargs['pk'])
        return super(GameReviewCreate, self).dispatch(request,
                                                      *args, **kwargs)

    def form_valid(self, form):
        form.instance.entry = self.entry
        return super(GameReviewCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(GameReviewCreate, self).get_context_data(**kwargs)
        context['game'] = self.game
        return context

    def get_success_url(self):
        return reverse('game_review_by_user',
                       kwargs={'slug': self.request.user.username, })


class GameReviewUpdate(PermissionMixin, UpdateView):
    model = GameReview
    form_class = GameReviewForm

    def get_success_url(self):
        return reverse('game_review_by_user',
                       kwargs={'slug': self.request.user.username, })


class GameReviewDelete(PermissionMixin, DeleteView):
    model = GameReview

    def get_success_url(self):
        return reverse('game_review_by_user',
                       kwargs={'slug': self.request.user.username, })


class GameReviewByUserView(ListView):
    model = GameReview
    template_name = 'app/review_by_user.html'

    def get_queryset(self):
        self.user_profile = get_object_or_404(
            User, username=self.kwargs['slug'])
        return GameReview.objects.filter(entry__user=self.user_profile)

    def get_context_data(self, **kwargs):
        context = super(GameReviewByUserView, self).get_context_data(**kwargs)
        context['object'] = self.user_profile
        context['reviews_page'] = True
        return context


class GameReviewByGameView(ListView):
    model = GameReview
    template_name = 'app/review_by_game.html'

    def get_queryset(self):
        self.game = gamesdb_api.get_game(id=self.kwargs['pk'])
        if self.game is None:
            raise Http404
        return GameReview.objects.filter(entry__game_id=self.game.id)

    def get_context_data(self, **kwargs):
        context = super(GameReviewByGameView, self).get_context_data(**kwargs)
        context['game'] = self.game
        context['reviews_page'] = True
        return context


class GameRecommendationCreate(EntryMixin, CreateView):
    model = GameRecommendation
    form_class = GameRecommendationForm

    def form_valid(self, form):
        similar = form.cleaned_data.get('similar')
        form.instance.entry1 = self.entry
        form.instance.entry2 = similar
        return super(GameRecommendationCreate, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(GameRecommendationCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['entry'] = self.entry
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(GameRecommendationCreate,
                        self).get_context_data(**kwargs)
        context['game_title'] = self.entry.game_title
        return context

    def get_success_url(self):
        return reverse('game_recommendation_by_user',
                       kwargs={'slug': self.request.user.username, })


class GameRecommendationUpdate(UpdateView):
    model = GameRecommendation
    form_class = GameRecommendationEditForm

    def get_success_url(self):
        return reverse('game_recommendation_by_user',
                       kwargs={'slug': self.request.user.username, })


class GameRecommendationByUserView(ListView):
    model = GameRecommendation
    template_name = 'app/recommendation_by_user.html'

    def get_queryset(self):
        self.user_profile = get_object_or_404(
            User, username=self.kwargs['slug'])
        return GameRecommendation.objects.filter(
            entry1__user=self.user_profile).distinct()

    def get_context_data(self, **kwargs):
        context = super(GameRecommendationByUserView,
                        self).get_context_data(**kwargs)
        context['object'] = self.user_profile
        context['recommendations_page'] = True
        return context


class GameRecommendationByGame(ListView):
    model = GameRecommendation
    template_name = 'app/recommendation_by_game.html'

    def get_queryset(self):
        game = gamesdb_api.get_game(id=self.kwargs['pk'])
        if game is None:
            raise Http404
        self.game = game
        return GameRecommendation.objects.filter(Q(entry1__game_id=game.id) |
                                                 Q(entry2__game_id=game.id))

    def get_context_data(self, **kwargs):
        context = super(GameRecommendationByGame,
                        self).get_context_data(**kwargs)
        context['game'] = self.game
        context['recommendations_page'] = True
        return context


class SearchResultsView(TemplateView):

    template_name = "app/search_results.html"

    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if q:
            games = gamesdb_api.get_games_list(name=q)
            context['games'] = games[:]
            games.sort(key=lambda x: x.platform)
            context['games_by_platform'] = games
        return context


class UserProfileUpdate(LoginRequiredMixin, UpdateView):

    model = UserProfile
    form_class = UserProfileForm
    template_name = 'app/userprofile_form.html'
    
    def get_object(self):
        return self.request.user.profile
