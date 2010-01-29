from datetime import datetime

from django.db import models
from django.core import urlresolvers
from django.contrib import databrowse

from apps.data.models import Data
from apps.people.models import Person, Band
from apps.images.models import Gallery, Image

class MusicData(Data):
    artwork = models.ForeignKey(Gallery, null=True, blank=True)
    official = models.BooleanField()

    def get_class_type(self):
        subclasses = ('song', 'release')
        for subclass in subclasses:
            if hasattr(self, subclass):
                return subclass
        return None

    def get_absolute_url(self):
        subclass = self.get_class_type()
        if subclass:
            return getattr(self, subclass).get_absolute_url()
        else:
            return None

    def get_human_class_type(self):
        classes = {
            'song': 'Song',
            'release': 'Release',
        }

        subclass = self.get_class_type()

        return classes.get(subclass)

    def get_template(self):
        subclass = self.get_class_type()
        if subclass:
            return getattr(self, subclass).get_template()
        else:
            return None

class Song(MusicData):
    band = models.ForeignKey(Band)
    file = models.FileField(upload_to='uploads/music')
    track_number = models.IntegerField(null=True, blank=True)
    composers = models.ManyToManyField(Person, null=True, blank=True)
    older_version = models.ForeignKey('self', null=True, blank=True, related_name='newer')
    newer_version = models.ForeignKey('self', null=True, blank=True, related_name='older')

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        url = urlresolvers.reverse('song', kwargs={'slug':self.slug})
        return url

    def get_template(self):
        return 'music/song.html'

class Release(MusicData):
    band = models.ForeignKey(Band)
    TYPE_CHOICES = (
        ('EP', 'EP'),
        ('LP', 'LP'),
        ('LI', 'Live Set'),
        )
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    songs = models.ManyToManyField(Song)
    buy_link = models.URLField(blank=True_

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        url = urlresolvers.reverse('release', kwargs={'slug':self.slug})
        return url

    def get_template(self):
        return 'music/release.html'

    def save(self):
        super(Release, self).save()
        for song in self.songs.all():
            song.published = False
            song.save()

class Archive(models.Model):
    release = models.ForeignKey(Release)
    archive = models.FileField(upload_to='uploads/music')
    file_type = models.CharField(max_length=20)

    def __unicode__(self):
        return '%s - %s' % (self.release.name, self.file_type)

class Stem(models.Model):
    release = models.ForeignKey(Release)
    archive = models.FileField(upload_to='uploads/music')
    description = models.CharField(max_length=50)

    def __unicode__(self):
        return '%s - %s' % (self.release.name, self.description)

class Credit(models.Model):
    song = models.ForeignKey(Song)
    name = models.ForeignKey(Person)
    instruments = models.CharField(max_length=70)

    def __unicode__(self):
        return '%s: %s - %s' % (self.song, self.name, self.instruments)
