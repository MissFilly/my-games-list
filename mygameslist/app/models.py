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


class Genre(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Platform(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Game(models.Model):
    title = models.CharField(_('Title'), max_length=300)
    synopsis = models.TextField(_('Synopsis'))
    genre = models.ManyToManyField(Genre)
    platform = models.ManyToManyField(Platform)
    developer = models.ManyToManyField(Company, verbose_name=_('Developer'),
                                       related_name='gameclaim_developers')
    publisher = models.ManyToManyField(Company, verbose_name=_('publisher'),
                                       related_name='gameclaim_publishers')
    release_date = models.DateField(_('First release date'))
    score = models.DecimalField(_('Score'), max_digits=4, decimal_places=2,
                                null=True, blank=True)
    cover_img = models.ImageField(upload_to='covers')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class ListEntry(models.Model):
    SCORE_CHOICES = (
        (10, '(10) {0}'.format(_('Masterpiece'))),
        (9, '(9) {0}'.format(_('Great'))),
        (8, '(8) {0}'.format(_('Very good'))),
        (7, '(7) {0}'.format(_('Good'))),
        (6, '(6) {0}'.format(_('Fine'))),
        (5, '(5) {0}'.format(_('Average'))),
        (4, '(4) {0}'.format(_('Bad'))),
        (3, '(3) {0}'.format(_('Very bad'))),
        (2, '(2) {0}'.format(_('Horrible'))),
        (1, '(1) {0}'.format(_('Appalling'))),
    )
    REPLAY_VALUE_CHOICES = (
        ('VH', _('Very high')),
        ('HI', _('High')),
        ('ME', _('Medium')),
        ('LO', _('Low')),
        ('VL', _('Very low')),
    )
    STATUS_CHOICES = (
        ('PL', _('Playing')),
        ('CO', _('Completed')),
        ('OH', _('On-hold')),
        ('DR', _('Dropped')),
        ('WA', _('Want to play')),
    )
    user = models.ForeignKey(User)
    game = models.ForeignKey(Game)
    status = models.CharField(_('Status'), max_length=2,
                              choices=STATUS_CHOICES)
    score = models.CharField(_('Score'), max_length=2,
                             choices=SCORE_CHOICES)
    replay_value = models.CharField(_('Replay value'), max_length=2,
                                    choices=REPLAY_VALUE_CHOICES)

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
