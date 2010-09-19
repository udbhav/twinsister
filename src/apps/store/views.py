from urllib import urlencode, unquote_plus
import urllib2

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponse

def success(request):
    post_data = {
        "cmd": "_notify-synch",
        "tx": request.GET['tx'],
        "at": settings.PAYPAL_PDT_TOKEN,
        }

    request = urllib2.urlopen(settings.PAYPAL_SUBMIT_URL, urlencode(post_data))
    response = request.read().split('\n')
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
