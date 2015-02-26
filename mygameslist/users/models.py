import os
import uuid

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from django_countries.fields import CountryField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit


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
        return reverse('users:detail', kwargs={'slug': self.user.username})

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
