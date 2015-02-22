from django.conf.urls import patterns, url
from .views import TopGames

urlpatterns = patterns(
    '',
    url(r'^$', TopGames.as_view(), name='top_games'),
)