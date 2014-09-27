from django import template
from gamesdb.api import API

register = template.Library()
gamesdb_api = API()


@register.assignment_tag
def get_game(pk):
    game = gamesdb_api.get_game(id=pk)
    return game
