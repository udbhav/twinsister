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
        shows = Show.objects.filter(show_date__gte=date_result).filter(published=True)
        tours = Tour.objects.annotate(
            sort_date = Min('shows__show_date'), 
            end_date = Max('shows__show_date')
            ).filter(end_date__gte=date_result)

        title = 'Shows'

    else:
        shows = Show.objects.filter(show_date__lte=date_result).filter(published=True)
        tours = Tour.objects.annotate(
            sort_date = Min('shows__show_date'), 
            end_date = Max('shows__show_date')
            ).filter(end_date__lte=date_result)

        title = 'Past Shows'

    result_list = sorted(
        chain(shows, tours),
        key=attrgetter('sort_date'))

    paginator = Paginator(result_list, 25)

    try:
        results = paginator.page(page)
    except (EmptyPage, InvalidPage):
        results = paginator.page(paginator.num_pages)

    return render_to_response('events/shows.html', {
            'object_list': results.object_list,
            'page_obj': results,
            'current_shows': current_shows,
            'title': title,
            }, context_instance=RequestContext(request))
            
