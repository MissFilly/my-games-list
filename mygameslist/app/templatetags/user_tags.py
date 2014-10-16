from django import template
from django.contrib.auth.models import User

from friendship.models import FriendshipManager

register = template.Library()


@register.assignment_tag
def user_is_friend(user_profile, request_user):
    if request_user.is_authenticated():
        fm = FriendshipManager()
        return fm.are_friends(user_profile, request_user)
    return False
