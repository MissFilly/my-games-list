from django import template
from django.contrib.auth.models import User
from django.templatetags.static import static

from friendship.models import FriendshipManager

from mygameslist.app.models import ListEntry

register = template.Library()


@register.assignment_tag
def user_is_friend(user_profile, request_user):
    if request_user.is_authenticated():
        fm = FriendshipManager()
        return fm.are_friends(user_profile, request_user)
    return False


@register.simple_tag
def avatar_or_default(user):
    avatar = user.profile.avatar
    if avatar:
        return avatar.url
    else:
        return static('img/default.png')


@register.assignment_tag
def user_game_entry(user, game_pk):
    if user.is_authenticated():
        try:
            return ListEntry.objects.get(user=user,
                                         game_id=game_pk)
        except ListEntry.DoesNotExist:
            pass
    return
