from datetime import timedelta

from django.db.models import Q, Count, Avg
from django.shortcuts import render, redirect
from django.http import Http404
from django.utils import timezone
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from gamesdb.api import API
from social.apps.django_app.default.models import UserSocialAuth
import steamapi

from .gamesdb_manager import get_or_create_game
from .models import *
from .forms import *
from .mixins import *

gamesdb_api = API()


def home(request):
    reviews = GameReview.objects_with_scores.order_by('-date_created')[:4]
    recommendations = GameRecommendation.objects_with_scores \
        .order_by('-date_created')[:4]
    last_month = timezone.now().date() - timedelta(days=30)
    top_month = ListEntry.objects.filter(date_created__gt=last_month) \
        .values('game_id', 'game__title', 'game__thumb_url') \
        .annotate(count=Count('game_id')).order_by('-count')[:5]
    context = dict(reviews=reviews, recommendations=recommendations,
                   top_month=top_month)
    return render(request, 'index.html', context)


class TopGames(ListView):
    model = ListEntry
    template_name = 'app/top_games.html'
    paginate_by = 25

    def get_queryset(self):
        return ListEntry.objects.filter(score__isnull=False) \
            .values('game_id', 'game__title', 'game__thumb_url') \
            .annotate(average=Avg('score'), count=Count('game_id')) \
            .order_by('-average')


class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    slug_field = 'username'

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        user = self.object
        context['reviews'] = GameReview.objects_with_scores \
            .filter(entry__user=user).order_by('-date_created')[:3]
        context['recommendations'] = GameRecommendation.objects_with_scores \
            .filter(entry1__user=user).distinct().order_by('-date_created')[:3]
        context['detail_page'] = True
        return context


class GameDetailView(DetailView):
    model = Game
    template_name = 'game_detail.html'
    slug_field = 'gamesdb_id'

    def get_object(self):
        try:
            return super(GameDetailView, self).get_object()
        except Http404:
            return get_or_create_game(self.kwargs.get('slug'))

    def get_context_data(self, **kwargs):
        context = super(GameDetailView, self).get_context_data(**kwargs)
        game = self.object
        reviews = GameReview.objects_with_scores.filter(
            entry__game_id=game.id).order_by('-date_created')[:3]
        recommendations = GameRecommendation.objects_with_scores.filter(
            Q(entry1__game_id=game.id) | Q(entry2__game_id=game.id)) \
            .distinct().order_by('-date_created')[:3]

        context.update(dict(reviews=reviews,
                            recommendations=recommendations,
                            detail_page=True))
        return context


class GameListByUserView(ListView):
    model = ListEntry
    template_name = 'game_list_by_user.html'

    def get_queryset(self):
        self.user_profile = get_object_or_404(
            User, username=self.kwargs['slug'])
        return ListEntry.objects.filter(user=self.user_profile)

    def get_context_data(self, **kwargs):
        context = super(GameListByUserView, self).get_context_data(**kwargs)
        context['user_profile'] = self.user_profile
        return context


class ListEntryCreate(LoginRequiredMixin, CreateView):
    model = ListEntry
    form_class = ListEntryForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.game = get_or_create_game(kwargs.get('slug'))
        try:
            entry = ListEntry.objects.get(user=request.user,
                                          game_id=self.game.id)
            return redirect(reverse('entry_update', kwargs={'pk': entry.pk, }))
        except ListEntry.DoesNotExist:
            pass
        return super(ListEntryCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.game = self.game
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
                review = GameReview.objects.get(
                    entry__game_id=kwargs['pk'],
                    entry__user=request.user)
                return redirect(reverse('review_update',
                                        kwargs={'pk': review.pk}))
            except:
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
        return GameReview.objects_with_scores.filter(
            entry__user=self.user_profile
        )

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
        return GameReview.objects_with_scores.filter(
            entry__game_id=self.game.id
        )

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


class GameRecommendationUpdate(PermissionMixin, UpdateView):
    model = GameRecommendation
    form_class = GameRecommendationEditForm

    def get_success_url(self):
        return reverse('game_recommendation_by_user',
                       kwargs={'slug': self.request.user.username, })


class GameRecommendationDelete(PermissionMixin, DeleteView):
    model = GameRecommendation

    def get_success_url(self):
        return reverse('game_recommendation_by_user',
                       kwargs={'slug': self.request.user.username, })


class GameRecommendationByUserView(ListView):
    model = GameRecommendation
    template_name = 'app/recommendation_by_user.html'

    def get_queryset(self):
        self.user_profile = get_object_or_404(
            User, username=self.kwargs['slug'])
        return GameRecommendation.objects_with_scores.filter(
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
        return GameRecommendation.objects_with_scores \
            .filter(Q(entry1__game_id=game.id) |
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
        search_type = self.request.GET.get('search_type')
        if q:
            if search_type == 'games':
                games = gamesdb_api.get_games_list(name=q)
                context['games'] = games[:]
                games.sort(key=lambda x: x.platform)
                context['games_by_platform'] = games
            else:
                query = User.objects.filter(username__icontains=q)
                context['users'] = query
        context['search_type'] = search_type
        context['query'] = q
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


class AjaxSearch(JSONResponseMixin, View):

    def get(self, request, *args, **kwargs):
        import time
        q = self.request.GET.get('name')
        start = time.time()
        context = dict(games=gamesdb_api.get_games_list(name=q),
                       success=True)
        end = time.time()
        print("\n\n\nGet games list time: " + str(end - start) + "\n\n\n")
        return self.render_to_response(context)


class ImportSteamGames(View):

    def get(self, request):
        try:
            steam_account = UserSocialAuth.objects.get(provider='steam',
                                                       user=self.request.user)
            steam_id = steam_account.extra_data['player']['steamid']
            games = steamapi.user.SteamUser(int(steam_id)).games
            for g in games:
                exists = ListEntry.objects.filter(user=request.user,
                                                  game_title=g.name).exists()
                if not exists:
                    gl = gamesdb_api.get_game(name=g.name, platform='PC')
                    if gl:
                        if not isinstance(gl, list):
                            if gl.title == g.name:
                                ListEntry.objects.create(
                                    user=request.user,
                                    game_id=gl.id,
                                    game_title=gl.title,
                                    game_thumb_url=gl.thumb_url,
                                    status='CO')
                        else:
                            for x in gl:
                                if x.title == g.name:
                                    ListEntry.objects.create(
                                        user=request.user,
                                        game_id=x.id,
                                        game_title=x.title,
                                        game_thumb_url=x.thumb_url,
                                        status='CO')
        except UserSocialAuth.DoesNotExist:
            pass
        return redirect('/')
