from datetime import timedelta

from django.db.models import Count
from django.shortcuts import render, redirect
from django.http import Http404
from django.utils import timezone, translation
from django.utils.translation import get_language
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from gamesdb.api import API
from social.apps.django_app.default.models import UserSocialAuth
import steamapi
from .gamesdb_manager import get_or_create_game, create_game
from .forms import *
from mygameslist.mixins import *

gamesdb_api = API()


def home(request):
    reviews = GameReview.objects_with_scores.order_by('-date_created')[:4]
    recommendations = GameRecommendation.objects_with_scores \
        .order_by('-date_created')[:4]
    last_month = timezone.now().date() - timedelta(days=30)
    top_month = ListEntry.objects.filter(date_created__gt=last_month) \
        .values('game__gamesdb_id', 'game__title', 'game__thumb_url') \
        .annotate(count=Count('game_id')).order_by('-count')[:5]
    context = dict(reviews=reviews, recommendations=recommendations,
                   top_month=top_month)
    return render(request, 'index.html', context)


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
        lang_info = translation.get_language_info(get_language())
        context['lang'] = lang_info.get('name')
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
                    entry__game__gamesdb_id=kwargs['slug'],
                    entry__user=request.user)
                return redirect(reverse('review_update',
                                        kwargs={'pk': review.pk}))
            except GameReview.DoesNotExist:
                self.game = get_or_create_game(kwargs.get('slug'))
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
        return reverse('users:detail', kwargs={'slug': self.request.user.username, })


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


class GameReviewByGameView(ListView):
    model = GameReview
    template_name = 'game_detail.html'

    def get_queryset(self):
        self.game = get_or_create_game(self.kwargs['slug'])
        if self.game is None:
            raise Http404
        return GameReview.objects_with_scores.filter(entry__game_id=self.game.id)

    def get_context_data(self, **kwargs):
        context = super(GameReviewByGameView, self).get_context_data(**kwargs)
        context['object'] = self.game
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
        context['game_title'] = self.entry.game.title
        return context

    def get_success_url(self):
        return reverse('users:recommendations', kwargs={'slug': self.request.user.username, })


class GameRecommendationUpdate(PermissionMixin, UpdateView):
    model = GameRecommendation
    form_class = GameRecommendationEditForm

    def get_success_url(self):
        return reverse('users:recommendations', kwargs={'slug': self.request.user.username, })


class GameRecommendationDelete(PermissionMixin, DeleteView):
    model = GameRecommendation

    def get_success_url(self):
        return reverse('users:recommendations', kwargs={'slug': self.request.user.username, })


class GameRecommendationByGame(ListView):
    model = GameRecommendation
    template_name = 'game_detail.html'

    def get_queryset(self):
        self.game = get_or_create_game(self.kwargs['slug'])
        if self.game is None:
            raise Http404
        return GameRecommendation.objects_with_scores.filter(Q(entry1__game_id=self.game.id) |
                                                             Q(entry2__game_id=self.game.id))

    def get_context_data(self, **kwargs):
        context = super(GameRecommendationByGame,
                        self).get_context_data(**kwargs)
        context['object'] = self.game
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
            steam_games = steamapi.user.SteamUser(int(steam_id)).games
            platform, created = Platform.objects.get_or_create(name='PC')
            # Get relevant data from Steam games (name and Steam ID)
            steam_data = {steam_game.name: steam_game.appid for steam_game in steam_games}

            try:
                steam_ids = steam_data.values()
                entries = Game.objects.values_list('steam_id', flat=True)\
                                      .filter(listentry__user=request.user, platform=platform, steam_id__in=steam_ids)
                # entries = ListEntry.object.values_list('steam_id', flat=True)\
                #                           .filter(user=request.user, game__steam_id__in=steam_ids)
                # Get Steam IDs that weren't included in user's list
                unknown_steam_ids = list(set(steam_ids)-set(entries))

                if unknown_steam_ids:
                    games_with_steam_id = Game.objects.values('id', 'steam_id')\
                                                      .filter(steam_id__in=unknown_steam_ids)
                    # Create a ListEntry for games that weren't in user's list but have `steam_id` not null
                    for game in games_with_steam_id:
                        ListEntry.objects.create(user=request.user, game_id=game['id'], status='CO')
                        unknown_steam_ids.remove(game['steam_id'])

                    if unknown_steam_ids:
                        known_steam_ids = list(set(steam_ids)-set(unknown_steam_ids))
                        # Get Games that don't have a Steam ID
                        games_without_steam_id = Game.objects.filter(title__in=steam_data.keys(), platform=platform)\
                                                             .exclude(steam_id__in=known_steam_ids)
                        for game in games_without_steam_id:
                            title = game.title
                            steam_id = steam_data.get(title)
                            game.steam_id = steam_id
                            game.save()
                            ListEntry.objects.get_or_create(user=request.user,
                                                            game=game, defaults={'status': 'CO'})
                            unknown_steam_ids.remove(steam_id)

                        if unknown_steam_ids:
                            unknown = {steam_name: steam_id for steam_name, steam_id in steam_data.items()
                                       if steam_id in unknown_steam_ids}
                            for steam_name, steam_id in unknown.items():
                                game = None
                                gl = gamesdb_api.get_game(name=steam_name, platform='PC')
                                if gl:
                                    if not isinstance(gl, list):
                                        gl = [gl]
                                    for x in gl:
                                        if x.title == steam_name:
                                            game = create_game(x)
                                            break
                                    if game is not None:
                                        game.steam_id = steam_id
                                        game.save()
                                        ListEntry.objects.create(user=request.user, game=game, status='CO')

            except UserSocialAuth.DoesNotExist:
                pass
            return redirect('/')

            # for steam_game in games:
            #     game = entry = None
            #     try:
            #         entry = ListEntry.objects.get(user=request.user,
            #                                       game__title=steam_game.name,
            #                                       game__platform=platform)
            #         game = entry.game
            #     except ListEntry.DoesNotExist:
            #         gl = gamesdb_api.get_game(name=steam_game.name, platform='PC')
            #         if gl:
            #             if not isinstance(gl, list):
            #                 if gl.title == steam_game.name:
            #                     game = get_or_create_game(gl.id)
            #             else:
            #                 for x in gl:
            #                     if x.title == steam_game.name:
            #                         game = get_or_create_game(x.id)
            #                         break
            #     if game is not None:
            #         game.steam_id = steam_game.appid
            #         game.save()
            #         ListEntry.objects.create(user=request.user, game=game, status='CO')
        except UserSocialAuth.DoesNotExist:
            pass
        return redirect('/')
