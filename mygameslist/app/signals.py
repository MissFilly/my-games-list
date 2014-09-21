from django.db.models.signals import m2m_changed
from django.core.exceptions import ValidationError
from .models import GameRecommendation


def regions_changed(sender, **kwargs):
    if kwargs['instance'].entries.count() > 2:
        raise ValidationError("You can't assign more than three regions")


m2m_changed.connect(regions_changed, sender=GameRecommendation.entries)
