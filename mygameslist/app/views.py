from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Game, GameReview, GameRecommendation, \
    UserProfile, ListEntry
from .forms import ListEntryForm, GameReviewForm
from .mixins import LoginRequiredMixin, GameReviewEntryMixin


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
        context['reviews'] = GameReview.objects.filter(entry__game=game)
        context['recommendations'] = GameRecommendation.objects.filter(
            Q(game1_entry__game=game) | Q(game2_entry__game=game))

        user = self.request.user
        if user.is_authenticated():
            context['entry'] = ListEntry.objects.get(user=user,
                                                     game=self.object)
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

    def dispatch(self, request, *args, **kwargs):
        self.game = get_object_or_404(Game, pk=kwargs['pk'])
        if request.user.is_authenticated():
            entry = ListEntry.objects.filter(user=request.user,
                                             game=self.game)
            if entry.exists():
                return redirect(reverse(
                    'entry_update',
                    kwargs={'pk': kwargs['pk'], }))
        return super(ListEntryCreate, self).dispatch(request,
                                                     *args, **kwargs)

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


class GameReviewCreate(GameReviewEntryMixin, CreateView):
    model = GameReview
    form_class = GameReviewForm

    # Uncomment to redirect to UpdateView if the review for this game and
    # user already exists.

    # def dispatch(self, request, *args, **kwargs):
    # if request.user.is_authenticated():
    #     try:
    #         review = GameReview.objects.get(entry__game__pk=kwargs['pk'],
    #                                         entry__user=request.user)
    #         return redirect(reverse('review_update',
    #                                 kwargs={'pk': review.pk}))
    #     except GameReview.DoesNotExist:
    #         pass
    # return super(GameReviewCreate, self).dispatch(request,
    #                                               *args, **kwargs)

    def form_valid(self, form):
        form.instance.entry = self.entry
        return super(GameReviewCreate, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(GameReviewCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(GameReviewCreate, self).get_context_data(**kwargs)
        context['game'] = self.entry.game
        return context


class GameReviewUpdate(UpdateView):
    model = GameReview
    form_class = GameReviewForm


class GameReviewByUser(ListView):
    pass
