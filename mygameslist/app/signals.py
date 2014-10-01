from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from .models import UserProfile


@receiver(user_signed_up)
def new_user_signup(sender, **kwargs):
    p = UserProfile(user=kwargs['user'])
    p.save()
    import pdb; pdb.set_trace()
