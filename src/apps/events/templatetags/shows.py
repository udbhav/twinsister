from datetime import datetime
from datetime import timedelta

from django import template

from apps.events.models import Show

register = template.Library()

@register.inclusion_tag('events/upcoming_shows.html')
def shows():
    shows = Show.objects.filter(show_date__gte=datetime.now()).order_by('show_date')[:5]
    return {'shows':shows}

@register.inclusion_tag('events/next_show.html')
def next_show():
    try:
        now = datetime.now()
        difference = timedelta(hours=4)
        date_result = now - difference
        show = Show.objects.filter(show_date__gte=date_result).order_by('show_date')[0]
    except IndexError:
        show = None
    return {'show':show}

@register.filter
def upcoming_show(show):
    if show.show_date > datetime.now():
        return True
    else:
        return False

@register.filter
def tour_shows(tour):
    return tour.shows.order_by('show_date')
