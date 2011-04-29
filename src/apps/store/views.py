from datetime import datetime
from urllib import urlencode, unquote_plus
from urlparse import parse_qs
import urllib2
import re
import os
import logging

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.core import urlresolvers

from apps.store.models import IpnMessage, Order

def success(request):
    post_data = {
        "cmd": "_notify-synch",
        "tx": request.GET['tx'],
        "at": settings.PAYPAL_PDT_TOKEN,
        }

    respnse = urllib2.urlopen(settings.PAYPAL_SUBMIT_URL, urlencode(post_data)).read().split('\n')
    response_data = {}

    if response[0] == 'SUCCESS':
        error = False

        for line in response:
            if line.find("=") != -1:
                split_data = line.split("=")
                response_data[split_data[0]] = unquote_plus(split_data[1])

        print response_data
    else:
        error = True

    return render_to_response('store/success.html', {
            'error': error,
            'response_data': response_data,
            }, context_instance=RequestContext(request))

def ipn(request):
    url = settings.PAYPAL_SUBMIT_URL + '?cmd=_notify-validate&' + request.META['QUERY_STRING']
    IpnMessage.objects.create(message=url)
    response = urllib2.urlopen(url)
    if response.read() == 'VERIFIED':
        message = parse_qs(request.META['QUERY_STRING'])

        # Log the entire message for records
        formatted_message = ''
        for k,v in message.items():
            formatted_message += '%s: %s\n' % (k, v)

        IpnMessage.objects.create(message=formatted_message)

        # If a customer placed an order
        if message['txn_type'] == 'web_accept':

            # Create the Order
            shipping_address = '%s\n%s\n%s, %s %s\n%s' % (
                message['address_name'],
                message['address_street'],
                message['address_city'],
                message['address_state'],
                message['address_zip'],
                message['address_country'],
                )

            product = Product.objects.get(pk=int(message['item_number']))

            Order.objects.create(
                customer_name = message['first_name'] + ' ' + message['last_name'],
                customer_email = message['payer_email'],
                transaction_id = message['txn_id'],
                timestamp = datetime.now(),
                shipping_address = shipping_address,
                quantity = message['quantity'],
                order_total = message['mc_gross'],
                )

            # Send emails to store admins
            # Send email to customer

            return HttpResponse("Everything is OK")

    else:
        return HttpResponse("Invalid transaction")

SHA1_RE = re.compile('^[a-f0-9]{40}$')

def _validate_key(download_key):
    error_message = "The download key is invalid."
    download_key = download_key.lower()

    if not SHA1_RE.search(download_key):
        return (False, error_message, None)

    try:
        dl_product = DownloadLink.objects.get(key=download_key)
    except:
        error_message = "The download key is invalid."
        return (False, error_message, None)

    if not dl_product.active:
        return (False, error_message, None)
    else:
        return (True, None, dl_product)

def process_download(request, download_key):
    valid, msg, dl_product = _validate_key(download_key)
    if not valid:
        context = RequestContext(request, {'error_message': msg})
        return render_to_response('store/download.html',context_instance=context)
    else:
        request.session['download_key'] = download_key
        url = urlresolvers.reverse('digital_download_send', kwargs= {'download_key': download_key})
        context = RequestContext(request, {'download_product': dl_product, 'dl_url' : url})
        return render_to_response('store/download.html', context_instance=context)

def send_file(request, download_key):
    """
    After the appropriate session variable has been set, we commence the download.
    The key is maintained in the url but the session variable is used to control the
    download in order to maintain security.
    """
    if not request.session.get('download_key', False):
        url = urlresolvers.reverse('digital_download_process', kwargs = {'download_key': download_key})
        return HttpResponseRedirect(url)
    valid, msg, dl_product = _validate_key(request.session['download_key'])
    if not valid:
        url = urlresolvers.reverse('digital_download_process', kwargs = {'download_key': request.session['download_key']})
        return HttpResponseRedirect(url)

    # some temp vars
    file = dl_product.get_file()
    file_url = '/%s' % file.name # create an absolute/root url

    # get file name from url
    file_name = os.path.basename(file_url)

    dl_product.active = False
    dl_product.save()

    del request.session['download_key']
    response = HttpResponse()
    # For Nginx
    response['X-Accel-Redirect'] = file_url
    # For Apache and Lighttpd v1.5
    response['X-Sendfile'] = file_url
    # For Lighttpd v1.4
    response['X-LIGHTTPD-send-file'] = file_url
    response['Content-Disposition'] = "attachment; filename=%s" % file_name
    response['Content-length'] =  file.size
    contenttype, encoding = mimetypes.guess_type(file_name)
    if contenttype:
        response['Content-type'] = contenttype
    return response
