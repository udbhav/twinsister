from django.db import models

from apps.music.models import Release, Song


class Product(models.Model):
    cost = models.DecimalField(max_digits=5, decimal_places=2)

    def get_child(self):
        subclasses = ('digitalsong', 'digitalrelease', 'physicalrelease',)
        for subclass in subclasses:
            if hasattr(self, subclass):
                return getattr(self, subclass)
        return None
    
class DigitalSong(Product):
    song = models.ForeignKey(Song)

class DigitalRelease(Product):
    release = models.ForeignKey(Release)
    format = models.CharField(max_length=100)
    file = models.FileField(upload_to='uploads/store')

    def __unicode__(self):
        return '%s - %s' % (self.release, self.format)

class PhysicalRelease(Product):
    release = models.ForeignKey(Release)
    format = models.CharField(max_length=100)

    def __unicode__(self):
        return '%s - %s' % (self.release, self.format)

class Order(models.Model):
    customer_name = models.CharField(max_length=200)
    timestamp = models.DateTimeField()
    shipping_address = models.TextField(blank=True)
    shipped = models.BooleanField()
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=1)

class DownloadLink(models.Model):
    product = models.ForeignKey(Product)
    key = models.CharField(max_length=40)
    active = models.BooleanField()
