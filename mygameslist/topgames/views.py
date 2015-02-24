from django.db.models import Count, Avg
from django.views.generic import ListView
from mygameslist.app.models import ListEntry

from .forms import PlatformForm


class TopGames(ListView):
    model = ListEntry
    template_name = 'app/top_games.html'
    paginate_by = 25

    def get_queryset(self):
        q = ListEntry.objects.filter(score__isnull=False)
        data = self.request.GET
        platform = data.get('platform')
        genre = data.get('genre')
        if platform:
            q = q.filter(game__platform=platform)
        if genre:
            q = q.filter(game__genre=genre)
        return q.values('game__gamesdb_id', 'game__title', 'game__thumb_url') \
                .annotate(average=Avg('score'), count=Count('game_id')) \
                .order_by('-average')

    def get_context_data(self, **kwargs):
        context = super(TopGames, self).get_context_data(**kwargs)
        context['platform_form'] = PlatformForm(self.request.GET)
        return context
