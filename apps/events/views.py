import datetime
from itertools import chain
from operator import attrgetter

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Min, Max
from django.shortcuts import render_to_response
from django.template import RequestContext

from apps.events.models import Show, Tour

def shows(request, page=1, current_shows=True):
    now = datetime.datetime.now()
    difference = datetime.timedelta(hours=7)
    date_result = now - difference

    if current_shows:
        shows = Show.objects.filter(show_date__gte=date_result).order_by('show_date')
        title = 'Shows'
    else:
        shows = Show.objects.filter(show_date__lte=date_result).order_by('-show_date')
        title = 'Past Shows'

    return render_to_response('events/shows.html', {
            'shows': shows,
            'current_shows': current_shows,
            'title': title,
            }, context_instance=RequestContext(request))
            
