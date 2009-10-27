from datetime import datetime

from django.db import models
from django.core import urlresolvers
from django.contrib import databrowse

from apps.people.models import Person, Band
from apps.images.models import Gallery, Image

class Data(models.Model):
    """
    An all-purpose container for all content on the site

    # Create some Data
    >>> from people.models import Person
    >>> person = Person.objects.create(name="Udbhav gupta")
    >>> Data.objects.create(name="Kickin' out the Jamz", slug="kickin-out-the-jamz", posted_by=person)
    <Data: Kickin' out the Jamz>
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    posted_by = models.ForeignKey(Person)
    pub_date = models.DateTimeField('date published', default=datetime.now())
    description = models.TextField(blank=True)
    header_image = models.ForeignKey(Image, blank=True, null=True)
    artwork = models.ManyToManyField(Gallery, null=True, blank=True)
    published = models.BooleanField(default=True)
    official = models.BooleanField()

    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        from apps.events.models import Show
        url = None
        try:
            self.song
            url = self.song.get_absolute_url()
        except Song.DoesNotExist:
            pass
        try:
            self.release
            url = self.release.get_absolute_url()
        except Release.DoesNotExist:
            pass
        try:
            self.show
            url = self.show.get_absolute_url()
        except Show.DoesNotExist:
            pass
        if not url:
            url = urlresolvers.reverse('entry', kwargs={'slug':self.slug})
        return url

    def get_class_type(self):
        from apps.events.models import Show
        class_type = None
        try:
            self.song
            class_type = 'Song'
        except Song.DoesNotExist:
            pass
        try:
            self.release
            class_type = 'Release'
        except Release.DoesNotExist:
            pass
        try:
            self.show
            class_type = 'Show'
        except Show.DoesNotExist:
            pass
        if not class_type:
            class_type = 'Entry'
        return class_type

    class Meta:
        verbose_name_plural = 'Entries'
        verbose_name = 'Entry'
        
class Song(Data):
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

class Release(Data):
    band = models.ForeignKey(Band)
    TYPE_CHOICES = (
        ('EP', 'EP'),
        ('LP', 'LP'),
        ('LI', 'Live Set'),
        )
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    songs = models.ManyToManyField(Song)

    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        url = urlresolvers.reverse('release', kwargs={'slug':self.slug})
        return url
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
