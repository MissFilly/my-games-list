from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(_('Name'), max_length=200)
    active = models.BooleanField(default=True)

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
    title = models.CharField(_('Title'), max_length=300)
    synopsis = models.TextField(_('Synopsis'))
    platform = models.CharField(_('Platform'), max_length=10)
    developer = models.ManyToManyField(Company, verbose_name=_('Developer'),
                                       related_name='gameclaim_developers')
    publisher = models.ManyToManyField(Company, verbose_name=_('publisher'),
                                       related_name='gameclaim_publishers')
    release_date = models.DateField(_('First release date'))
    score = models.DecimalField(_('Score'), max_digits=4, decimal_places=2,
                                null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class ListEntry(models.Model):
    user = models.ForeignKey(User)
    game = models.ForeignKey(Game)
    score = models.IntegerField(_('Score'))

    class Meta:
        verbose_name_plural = 'list entries'

    def __str__(self):
        return "{0}'s entry for {1}".format(self.user.username,
                                            self.game.title)


class GameReview(models.Model):
    user = models.ForeignKey(User)
    game = models.ForeignKey(Game)
    text = models.TextField(_('Text'))
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0}'s review for {1}".format(self.user.username,
                                             self.game.title)


class GameRecommendation(models.Model):
    user = models.ForeignKey(User)
    game1 = models.ForeignKey(Game, related_name='gamerecommendation_game1')
    game2 = models.ForeignKey(Game, related_name='gamerecommendation_game2')
    text = models.TextField(_('Text'))
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0}'s review for {1} - {2}".format(
               self.user.username, self.game1.title, self.game2.title)
