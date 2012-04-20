from datetime import datetime, timedelta
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
from django.db.models.signals import post_save, pre_save
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
from django.core.mail import EmailMultiAlternatives
from django.core import urlresolvers
from django.contrib.sites.models import Site
from django import forms

from apps.music.models import Release, Song
from apps.store.storages import ProductStorage

class Product(models.Model):
    cost = models.DecimalField(max_digits=5, decimal_places=2)
    release_date = models.DateTimeField(default=datetime.now())

    def get_child(self):
        subclasses = ('digitalsong', 'digitalrelease', 'physicalrelease',)
        for subclass in subclasses:
            if hasattr(self, subclass):
                return getattr(self, subclass)
        return None

    def __unicode__(self):
        return self.get_child().__unicode__()

    def released(self):
        if datetime.now() > self.release_date:
            return True
        else:
            return False

    def ready_to_ship(self):
        if datetime.now() - self.release_date > timedelta(days=-3):
            return True
        else:
            return False
    
class DigitalSong(Product):
    song = models.OneToOneField(Song)

    def __unicode__(self):
        return self.song.name

fs = ProductStorage()

class DigitalRelease(Product):
    release = models.ForeignKey(Release)
    format = models.CharField(max_length=100)
    file = models.FileField(upload_to='uploads/store', storage=fs)

    def __unicode__(self):
        return '%s - %s' % (self.release, self.format)

    def generate_link(self, time):
        return self.file.storage.bucket.get_key(self.file.name).generate_url(time, method='GET', query_auth=True)

class PhysicalRelease(Product):
    release = models.ForeignKey(Release)
    format = models.CharField(max_length=100)
    inventory = models.IntegerField(default=0)

    def __unicode__(self):
        return '%s - %s' % (self.release, self.format)

class DownloadLink(models.Model):
    order = models.OneToOneField('Order')
    key = models.CharField(max_length=40, unique=True)
    active = models.BooleanField(default=True)
    first_accessed = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.order.customer_name + ' - ' + self.order.product.__unicode__()

    def create_key(self):
        salt = sha_constructor(str(random.random())).hexdigest()[:5]
        download_key = sha_constructor(salt+smart_str(self.order.product.__unicode__())).hexdigest()
        return download_key

    def get_full_url(self):
        url = urlresolvers.reverse('store_download', kwargs= {'download_key': self.key})
        return('http://%s%s' % (Site.objects.get_current(), url))

    def save(self, *args, **kwargs):
        if not self.key:
            valid_key = False

            while not valid_key:
                proposed_key = self.create_key()
                try:
                    DownloadLink.objects.get(key=proposed_key)
                except ObjectDoesNotExist:
                    valid_key = True
                    
            self.key = proposed_key

        super(DownloadLink, self).save(*args, **kwargs)

STATUS_CHOICES = (
    ('w', 'Waiting for Payment'),
    ('u', 'Unreleased'),
    ('rs', 'Ready To Ship'),
    ('sn', 'Shipped No Digital'),
    ('ud', 'Unshipped Digital'),
    ('s', 'Shipped'),
    ('c', 'Complete'),
)

TYPE_CHOICES = (
    ('p', 'Physical Only'),
    ('b', 'Physical and Digital'),
    ('d', 'Digital'),
)

class Order(models.Model):
    customer_name = models.CharField(max_length=129)
    customer_email = models.EmailField()
    transaction_id = models.CharField(max_length=40)
    timestamp = models.DateTimeField()
    shipping_address = models.TextField(blank=True)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=1)
    order_total = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    shipping = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, blank=True)
    payment_status = models.CharField(max_length=20)
    order_type = models.CharField(max_length=1, choices=TYPE_CHOICES)

    def __unicode__(self):
        return self.customer_name

    def digital_media(self):
        if hasattr(self.product, 'digitalrelease'):
            return True

        if hasattr(self.product, 'digitalsong'):
            return True

        if hasattr(instance.product, 'physicalrelease'):
            releases = DigitalRelease.objects.filter(release=instance.product.release)
            if releases:
                return True

        return False

    def subtotal(self):
        return self.order_total - self.shipping - self.tax

    def save_physical(self):
        send_email = False
        subject = None
        body = None
        
        if not self.status:
            # We haven't processed this yet, so we have to send an email of some sort
            send_email = True
            subject = "Thanks For Your Order"

            if self.product.ready_to_ship():
                # We're ready to ship, send an email saying thanks, your order will ship soon
                body = "Thanks for your order, we'll be shipping it to you as soon as we can!"
                self.status = 'rs'

            else:
                # Unreleased, send an email thanking them for their preorder
                body = "Thanks for your preorder, we'll be shipping it right around %s." % self.product.release_date.strftime('%m %d')
                self.status = 'u'

        elif self.status == 'w':
            # They paid!
            if datetime.now() - self.product.release_date > timedelta(days=-3):
                # We're ready to ship
                self.status = 'rs'

            else:
                # Mark as unreleased
                self.status = 'u'

        elif self.status == 's':
            # It's shipped, send an email saying so
            self.status = 'c'
            send_email = True
            subject = "Your Order Has Shipped"
            body = "We just shipped your order.  It should be arriving really soon!"

        elif self.status == 'u':
            # If we're ready to ship, mark as such
            if self.product.ready_to_ship():
                self.status = 'rs'

        return send_email, subject, body

    def save_digital(self):
        send_email = False
        subject = None
        body = None

        if not self.status:
            # We haven't processed this yet, let's send an email
            send_email = True
            subject = "Thanks For Your Order"

            if self.product.released():
                # Send digital download, mark as complete
                self.status = 'c'
                body = "Thanks for your order. Your download is below."

            else:
                # Email thanking them for their order
                body = "Thanks for your order.  We'll be sending you a download link on %s" % self.product.release_date.strftime('%m %d')
                self.status = 'u'

        else:
            if self.product.released():
                # Send digital download, mark as complete
                send_email = True
                subject = "Your Download"
                self.status = 'c'

        return send_email, subject, body

    def save_physical_and_digital(self):
        send_email = False
        subject = None
        body = None

        if not self.status:
            # We haven't processed this yet, so let's send an email
            send_email = True
            subject = "Thanks For Your Order"

            if self.product.released():
                # Send an email with digital goods
                body = "Thanks for your order.  We'll be shipping it soon.  In the meantime, enjoy the download below!"
                self.status = 'rs'

            elif self.product.ready_to_ship():
                # Send an email w/out digital goods
                body = "Thanks for your order.  We'll be shipping it soon, and will also be sending you a digital download on %s" % self.product.release_date.strftime('%m %d')
                self.status = 'rs'

            else:
                # Send an email thanking them for their preorder
                body = "Thanks for your pre-order.  We'll be shipping right around %s.  You will also receive your free download then." % self.product.release_date.strftime('%m %d')
                self.status = 'u'

        elif self.status == 'u':
            # It's unreleased, let's check if it has been released in the interim
            if self.product.released():
                # Send an email with digital goods
                send_email = True
                subject = "Your Download"
                self.status = 'rs'

        elif self.status == 'rs':
            if self.product.released():
                # Send an email with digital goods, mark as unshipped and digital
                send_email = True
                subject = "Your Download"
                self.status = 'ud'

        elif self.status == 's':
            # Email and tell them their order shipped
            send_email = True
            subject = "Your Order Has Shipped"
            body = "We just shipped your order.  It should be arriving really soon."

            if not self.product.released():
                self.status = 'sn'

            else:
                self.satus = 'c'

        elif self.status == 'sn':
            # Shipped no digital, if released, send digital goods
            if self.product.released():
                send_email = True
                subject = "Your Download"
                self.status = 'c'

        elif self.status == 'w':
            # They paid, hurray!
            if self.product.released():
                # Send an email with digital goods
                send_email = True
                subject = "Your Download"
                self.status = 'rs'

            elif self.product.ready_to_ship():
                self.status = 'rs'

            else:
                self.status = 'u'

        return send_email, subject, body

    def save(self, *args, **kwargs):
        # This feels needlessly complicated, how else do I do decision trees?
        send_email = False

        if not self.status and (self.order_type == 'd' or self.order_type == 'b'):
            create_download_link = True
        else:
            create_download_link = False

        if self.status == 'c':
            # Order is complete, don't do anything
            pass

        elif self.payment_status != "Completed" and not self.status:
            # Send an email, Thanks for your order, we're waiting on payment to clear to act
            self.status = 'w'
            send_email = True
            subject = "Thanks For Your Order"
            body = "Thanks for your order.  We're waiting for your payment to clear before processing your order."

        elif self.payment_status != "Completed" and self.status:
            # Don't do anything, still waiting for this dude to pay up
            pass

        else:
            if self.order_type == 'p':
                send_email, subject, body = self.save_physical()
            elif self.order_type == 'd':
                send_email, subject, body = self.save_digital()
            elif self.order_type == 'b':
                send_email, subject, body = self.save_physical_and_digital()

        super(Order, self).save(*args, **kwargs)

        if create_download_link:
            download_link = DownloadLink.objects.create(order=self)
        else:
            try:
                download_link = DownloadLink.objects.get(order=self)
            except ObjectDoesNotExist:
                download_link = None

        if send_email:
            context = {'order': self, 'body': body, 'download_link': download_link}

            text_content = render_to_response('store/order_email.txt', context)
            html_content = render_to_response('store/order_email.html', context)

            msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [self.customer_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

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

            if hasattr(product, 'physicalrelease'):
                physical = True
            else:
                physical = False

            try:
                digital_releases = DigitalRelease.objects.filter(release=product.physicalrelease.release)
            except ObjectDoesNotExist:
                digital_releases = None

            if physical and not digital_releases:
                order_type = 'p'
            elif physical and digital_releases:
                order_type = 'b'
            else:
                order_type = 'd'

            Order.objects.create(
                customer_name = message['first_name'] + ' ' + message['last_name'],
                customer_email = message['payer_email'],
                transaction_id = message['txn_id'],
                timestamp = datetime.now(),
                shipping_address = shipping_address,
                quantity = message['quantity'],
                order_total = message['mc_gross'],
                shipping = message['shipping'],
                tax = message['tax'],
                product = product,
                payment_status = message['payment_status'],
                status = '',
                order_type = order_type,
                )

class InventoryForm(forms.ModelForm):
    class Meta:
        model = PhysicalRelease
        fields = ('inventory',)
