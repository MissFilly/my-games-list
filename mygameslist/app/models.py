from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(_('Name'), max_length=200)

    class Meta:
        verbose_name_plural = 'companies'

    def __str__(self):
        return self.name


class Game(models.Model):
    PLATFORM_CHOICES = (
        ('PS', 'PlayStation'),
        ('PS2', 'PlayStation 2'),
        ('PS3', 'PlayStation 3'),
        ('PS4', 'PlayStation 4'),
        ('PSP', 'PSP'),
        ('PSVITA', 'PlayStation Vita'),
        ('XBOX', 'Xbox'),
        ('XBOX360', 'Xbox 360'),
        ('XBOXONE', 'Xbox One'),
        ('WII', 'Wii'),
        ('WIIU', 'Wii U'),
        ('3DS', '3DS'),
        ('PC', 'PC'),
    )
    title = models.CharField(max_length=300, verbose_name=_('Title'))
    synopsis = models.TextField()
    platform = models.CharField(max_length=10)
    developer = models.ManyToManyField(Company, verbose_name=_('Developer'),
                                       related_name='gameclaim_developers')
    publisher = models.ManyToManyField(Company, verbose_name=_('publisher'),
                                       related_name='gameclaim_publishers')
    release_date = models.DateField(_('First release date'))
    score = models.DecimalField(_('Score'), max_digits=4, decimal_places=2,
                                null=True, blank=True)

    def __str__(self):
        return self.title


class ListEntry(models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'))
    game = models.ForeignKey(Game, verbose_name=_('Game'))
    score = models.IntegerField(_('Score'))
    review = models.TextField(_('Review'))

    def __str__(self):
        return "{0}'s {1} entry".format(self.user.username, game.title)
