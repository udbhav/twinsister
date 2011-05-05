from datetime import datetime
import random
import json
import logging

from django.db import models
from django.utils.hashcompat import sha_constructor
from django.utils.encoding import smart_str
from django.core.files.storage import FileSystemStorage
from django.dispatch import receiver
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist

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
    shipping_total = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20)

class IpnMessage(models.Model):
    message = models.TextField(editable=False)
    timestamp = models.DateTimeField(default=datetime.now(), editable=False)
    transaction_id = models.CharField(max_length=40, editable=False)

    def __unicode__(self):
        return self.transaction_id

    def formatted(self):
        message_dict = json.loads(self.message)
        s = ''
        for k,v in message_dict.items():
            s += '%s: %s<br/>' % (k, v)
        return s
    formatted.allow_tags = True

@receiver(post_save, sender=IpnMessage)
def ipn_listener(sender, instance, created, **kwargs):
    if created:

        message = json.loads(instance.message)
        valid = True

        # Make sure it's for the right merchant
        if message['business'] != settings.PAYPAL_RECEIVER_EMAIL:
            valid = False

        # Make sure it's not a duplicate
        try:
            order = Order.objects.get(transaction_id=message['txn_id'])
        except ObjectDoesNotExist:
            pass
        else:
            # if it's an existing order, we need to update the payment status
            order.payment_status = message['payment_status']
            order.save()
            valid = False

        # Make sure the product exists and the price is right
        try:
            product = Product.objects.get(pk=int(message['item_number']))
        except ObjectDoesNotExist:
            valid = False
        else:
            product_price = (float(message['mc_gross']) - float(message['shipping']) - float(message['tax'])) / float(message['quantity'])
            if product_price != float(product.cost):
                valid = False

        # Make sure it's a buy now order
        if message['txn_type'] != 'web_accept':
            valid = False

        if valid:

            # Create the Order
            try:
                shipping_address = '%s\n%s\n%s, %s %s\n%s' % (
                    message['address_name'],
                    message['address_street'],
                    message['address_city'],
                    message['address_state'],
                    message['address_zip'],
                    message['address_country'],
                    )
            except KeyError:
                shipping_address = ''

            product = Product.objects.get(pk=int(message['item_number']))

            Order.objects.create(
                customer_name = message['first_name'] + ' ' + message['last_name'],
                customer_email = message['payer_email'],
                transaction_id = message['txn_id'],
                timestamp = datetime.now(),
                shipping_address = shipping_address,
                quantity = message['quantity'],
                order_total = message['mc_gross'],
                shipping_total = message['shipping'],
                product = product,
                payment_status = message['payment_status'], 
                )

            # Send emails to store admins
            # Send email to customer
                               
    else:
        pass
    
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
