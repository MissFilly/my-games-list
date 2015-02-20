from django.http import Http404
from gamesdb.api import API
from .models import Platform, Genre, Company, Game

gamesdb_api = API()


def get_or_create_game(gamesdb_id):
    try:
        return Game.objects.get(gamesdb_id=gamesdb_id)
    except Game.DoesNotExist:
        gamesdb_game = gamesdb_api.get_game(id=gamesdb_id)
        if gamesdb_game is None:
            raise Http404
        platform, created = Platform.objects.get_or_create(name=gamesdb_game.platform)
        game = Game.objects.create(title=gamesdb_game.title,
                                   gamesdb_id=gamesdb_game.id,
                                   overview=gamesdb_game.overview,
                                   thumb_url=gamesdb_game.thumb_url)
        genres = []
        if gamesdb_game.genres:
            for g in gamesdb_game.genres:
                genre, created = Genre.objects.get_or_create(name=g.text)
                genres.append(genre)
        game.genre.add(*genres)
        if gamesdb_game.publisher:
            publisher, created = Company.objects.get_or_create(name=gamesdb_game.publisher)
            game.publisher.add(publisher)
        if gamesdb_game.developer:
            developer, created = Company.objects.get_or_create(name=gamesdb_game.developer)
            game.developer.add(developer)
        game.platform.add(platform)
        return game