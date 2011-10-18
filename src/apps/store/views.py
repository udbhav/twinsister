from datetime import datetime, timedelta
from urllib import urlencode, unquote_plus
from urlparse import parse_qs
import urllib2
import re
import os
import logging
import json

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.core import urlresolvers
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import DetailView, ListView
from django.contrib.auth.decorators import login_required

from apps.store.models import IpnMessage, Order, Product, DigitalRelease, DownloadLink
from apps.music.models import Release, Song

class BuyReleaseView(DetailView):
    template_name = 'store/buy.html'
    model = Release

class StoreAdminView(ListView):
    template_name = 'store/admin.html'
    queryset = Order.objects.filter(status='rs').order_by('-timestamp')

class CompletedOrdersView(ListView):
    template_name = 'store/completed_orders.html'
    queryset = Order.objects.filter(status='c').order_by('-timestamp')

class OrderDetailView(DetailView):
    template_name = 'store/order.html'
    model = Order

@login_required
def ship_order(request):
    if request.method == 'POST':
        order = get_object_or_404(Order, pk=request.POST['pk'])
        order.status = 's'
        order.save()
        return HttpResponse('OK!')
    else:
        return HttpResponseBadRequest('Bad Request')
        

def success(request):
    post_data = {
        "cmd": "_notify-synch",
        "tx": request.GET['tx'],
        "at": settings.PAYPAL_PDT_TOKEN,
        }

    response = urllib2.urlopen(settings.PAYPAL_SUBMIT_URL, urlencode(post_data)).read().split('\n')
    response_data = {}

    if response[0] == 'SUCCESS':
        error = False

        for line in response:
            if line.find("=") != -1:
                split_data = line.split("=")
                response_data[split_data[0]] = unquote_plus(split_data[1])

    else:
        error = True

    return render_to_response('store/success.html', {
            'error': error,
            'response_data': response_data,
            }, context_instance=RequestContext(request))

def ipn(request):
    message = request.POST
    url = settings.PAYPAL_SUBMIT_URL + 'cmd=_notify-validate&' + urlencode(message)
    response = urllib2.urlopen(url)

    if response.read() == 'VERIFIED':
        # Log the entire message for records
        message_dict = {}
        for k,v in message.items():
            message_dict[k] = v

        IpnMessage.objects.create(message=json.dumps(message_dict), transaction_id=message['txn_id'])
        return HttpResponse("Everything is OK")

    else:
        return HttpResponseBadRequest("Invalid transaction")

SHA1_RE = re.compile('^[a-f0-9]{40}$')

def _validate_key(download_key):
    download_key = download_key.lower()

    if not SHA1_RE.search(download_key):
        return (False, None)

    try:
        link = DownloadLink.objects.get(key=download_key)
    except ObjectDoesNotExist:
        return (False, None)

    if not link.active:
        return (False, None)

    if link.first_accessed:
        if datetime.now() - link.first_accessed > timedelta(hours=6):
            link.active = False
            link.save()
            return (False, None)

    return (True, link)

def download(request, download_key):
    valid, link = _validate_key(download_key)

    if not valid:
        context = RequestContext(request, {'error': True})
        return render_to_response('store/download.html',context_instance=context)
    else:
        request.session['download_key'] = download_key

        product = link.order.product

        download_url = None
        download_urls = []

        if hasattr(product, 'physicalrelease'):
            digital_releases = DigitalRelease.objects.filter(release=product.physicalrelease.release)

            if len(digital_releases) == 1:
                download_url = urlresolvers.reverse('store_process_download', kwargs={'download_key': download_key, 'product_id': digital_releases[0].pk})
            else:
                for digi_release in digital_releases:
                    url = urlresolvers.reverse('store_process_download', kwargs={'download_key': download_key, 'product_id': digi_release.pk})
                    download_urls.append({'name': digi_release.__unicode__(), 'url': url})
        else:
            download_url = urlresolvers.reverse('store_process_download', kwargs={'download_key': download_key, 'product_id': product.pk})

        context = RequestContext(request, {'download_url': download_url, 'download_urls': download_urls})
        return render_to_response('store/download.html', context_instance=context)

def process_download(request, download_key, product_id):
    if not request.session.get('download_key', False):
        url = urlresolvers.reverse('store_download', kwargs = {'download_key': download_key})
        return HttpResponseRedirect(url)

    valid, link = _validate_key(download_key)

    if not link.first_accessed:
        link.first_accessed = datetime.now()
        link.save()

    if not valid:
        context = RequestContext(request, {'error': True})
        return render_to_response('store/download.html',context_instance=context)
    else:
        product = link.order.product

        if hasattr(product, 'digitalrelease'):
            return HttpResponseRedirect(product.digitalrelease.file.url)
        elif hasattr(product, 'digitalsong'):
            return HttpResponseRedirect(product.digitalsong.song.download_url())
        elif hasattr(product, 'physicalrelease'):
            try:
                digi_release = DigitalRelease.objects.filter(release=product.physicalrelease.release, pk=product_id)[0]
            except IndexError:
                context = RequestContext(request, {'error': True})
                return render_to_response('store/download.html', context_instance=context)
            else:
                return HttpResponseRedirect(digi_release.file.url)
