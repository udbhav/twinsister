from datetime import datetime
import random

from django.db import models
from django.utils.hashcompat import sha_constructor
from django.utils.encoding import smart_str
from django.core.files.storage import FileSystemStorage

from apps.music.models import Release, Song

class Product(models.Model):
    cost = models.DecimalField(max_digits=5, decimal_places=2)

    def get_child(self):
        subclasses = ('digitalsong', 'digitalrelease', 'physicalrelease',)
        for subclass in subclasses:
            if hasattr(self, subclass):
                return getattr(self, subclass)
        return None

    def __unicode__(self):
        return self.get_child().__unicode__()

    def create_key(self):
        salt = sha_constructor(str(random.random())).hexdigest()[:5]
        download_key = sha_constructor(salt+smart_str(self.__unicode__())).hexdigest()
        return download_key

    
class DigitalSong(Product):
    song = models.ForeignKey(Song)

    def __unicode__(self):
        return self.song.name

fs = FileSystemStorage()

class DigitalRelease(Product):
    release = models.ForeignKey(Release)
    format = models.CharField(max_length=100)
    file = models.FileField(upload_to='uploads/store', storage=fs)

    def __unicode__(self):
        return '%s - %s' % (self.release, self.format)

class PhysicalRelease(Product):
    release = models.ForeignKey(Release)
    format = models.CharField(max_length=100)

    def __unicode__(self):
        return '%s - %s' % (self.release, self.format)

class Order(models.Model):
    customer_name = models.CharField(max_length=129)
    customer_email = models.EmailField()
    transaction_id = models.CharField(max_length=40)
    timestamp = models.DateTimeField()
    shipping_address = models.TextField(blank=True)
    shipped = models.BooleanField()
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=1)
    order_total = models.DecimalField(max_digits=10, decimal_places=2)

class IpnMessage(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(default=datetime.now())
    
class DownloadLink(models.Model):
    order = models.ForeignKey(Order)
    key = models.CharField(max_length=40)
    active = models.BooleanField()

    def get_file(self):
        product = self.order.product.get_child()

        if product.__class__ == DigitalSong:
            return product.song.file
        elif product.__class__ == DigitalRelease:
            return product.file
        else:
            try:
                digitalrelease = product.release.digitalrelease_set.all()[0]
            except:
                return None

            return digitalrelease.file
