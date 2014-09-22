from django.db.models.signals import m2m_changed
from django.core.exceptions import ValidationError
from .models import GameRecommendation, UserProfile


def regions_changed(sender, **kwargs):
    if kwargs['instance'].entries.count() > 2:
        raise ValidationError("You can't assign more than three regions")


m2m_changed.connect(regions_changed, sender=GameRecommendation.entries)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
