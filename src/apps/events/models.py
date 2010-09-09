from datetime import datetime

from django.db import models
from django.core import urlresolvers

from apps.people.models import Band
from apps.music.models import Data

class Venue(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class Show(Data):
    venue = models.ForeignKey(Venue)
    show_date = models.DateTimeField('Date & Time')
    cost = models.CharField(max_length=10, null=True, blank=True)
    bands = models.ManyToManyField(Band, null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super(Show, self).__init__(*args, **kwargs)
        self.sort_date = self.show_date

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        url = urlresolvers.reverse('show', kwargs={'slug':self.slug})
        return url

    def get_template(self):
        return 'events/show.html'

    class Meta:
        ordering = ('-show_date',)

class Tour(Data):
    shows = models.ManyToManyField(Show)
    def get_absolute_url(self):
        url = urlresolvers.reverse('tour', kwargs={'slug':self.slug})
        return url

    def get_template(self):
        return 'events/tour.html'

    def save(self):
        super(Tour, self).save()
        for show in self.shows.all():
            show.published = False
            show.save()
