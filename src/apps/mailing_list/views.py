from django.shortcuts import render_to_response
from django import http
from django.core import urlresolvers
from django.template import RequestContext

from apps.mailing_list.models import Subscriber, SubscriberForm

def subscribe(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect(urlresolvers.reverse('subscription_complete'))
    else:
        form = SubscriberForm()

    return render_to_response('mailing_list/subscribe.html', {
            'form' : form,
            }, context_instance=RequestContext(request))

