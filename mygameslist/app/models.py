import os
import uuid

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django_countries.fields import CountryField
from django.db import models
from django.utils.translation import ugettext as _

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from qhonuskan_votes.models import (VotesField, ObjectsWithScoresManager,
                                    SortByScoresManager)


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{0}.{1}'.format(uuid.uuid4(), ext)
    return os.path.join('avatars', filename)


class UserProfile(models.Model):
    GENDER_CHOICES = (('F', _('Female')), ('M', _('Male')))
    avatar = ProcessedImageField(upload_to=get_file_path,
                                 blank=True, null=True,
                                 processors=[ResizeToFit(265, 320)],
                                 format='JPEG',
                                 options={'quality': 90},
                                 verbose_name=_('Avatar'))
    user = models.OneToOneField(User)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,
                              verbose_name=_('Gender'))
    country = CountryField()
    about = models.TextField(verbose_name=_('About'), blank=True, null=True)

    def save(self, *args, **kwargs):
        # Delete old avatar if new avatar was saved
        try:
            this = UserProfile.objects.get(id=self.id)
            if this.avatar != self.avatar:
                this.avatar.delete(save=False)
        except:
            pass
        super(UserProfile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'slug': self.user.username})

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


class Platform(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    title = models.CharField(max_length=200)
    thumb_url = models.URLField(null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    gamesdb_id = models.PositiveIntegerField(null=True, blank=True, unique=True)
    steam_id = models.PositiveIntegerField(null=True, blank=True, unique=True)
    platform = models.ManyToManyField(Platform, null=True, blank=True)
    genre = models.ManyToManyField(Genre, null=True, blank=True)
    developer = models.ManyToManyField(Company, null=True, blank=True, related_name='game_developer')
    publisher = models.ManyToManyField(Company, null=True, blank=True, related_name='game_publisher')
    release_date = models.DateField(null=True, blank=True)

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
    score = models.IntegerField(_('Score'), choices=SCORE_CHOICES,
                                null=True, blank=True)
    replay_value = models.CharField(_('Replay value'), max_length=2,
                                    choices=REPLAY_VALUE_CHOICES,
                                    null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'list entries'
        unique_together = ('user', 'game')

    def __str__(self):
        return "{0}'s entry for {1}".format(self.user.username,
                                            self.game_id)


class GameReview(models.Model):
    entry = models.OneToOneField(ListEntry)
    text = models.TextField(_('Text'))
    date_created = models.DateTimeField(auto_now_add=True)
    votes = VotesField()
    objects = models.Manager()
    objects_with_scores = ObjectsWithScoresManager()
    sort_by_score = SortByScoresManager()

    def __str__(self):
        return "{0}'s review for {1}".format(self.entry.user.username,
                                             self.entry.game_id)


class GameRecommendation(models.Model):
    entry1 = models.ForeignKey(ListEntry, related_name='recommendation_entry1')
    entry2 = models.ForeignKey(ListEntry, related_name='recommendation_entry2')
    text = models.TextField(_('Text'))
    date_created = models.DateTimeField(auto_now_add=True)
    votes = VotesField()
    objects = models.Manager()
    objects_with_scores = ObjectsWithScoresManager()
    sort_by_score = SortByScoresManager()

    class Meta:
        unique_together = ('entry1', 'entry2')

    def __str__(self):
        return "{0}'s recommendation for {1} - {2}".format(
            self.entry1.user.username,
            self.entry1.game_id,
            self.entry2.game_id)

    def save(self, *args, **kwargs):
        if self.entry1.game_id > self.entry2.game_id:
            self.entry1, self.entry2 = self.entry2, self.entry1
        super(GameRecommendation, self).save(*args, **kwargs)
