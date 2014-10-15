from django import template

from friendship.models import FriendshipRequest

register = template.Library()


@register.assignment_tag
def get_notifications(user):
    requests = FriendshipRequest.objects.filter(to_user=user,
                                                viewed__isnull=True)
    return requests.count()
