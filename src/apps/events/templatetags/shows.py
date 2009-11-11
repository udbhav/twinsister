from datetime import datetime

from django import template

from apps.events.models import Show

register = template.Library()

@register.inclusion_tag('events/upcoming_shows.html')
def shows():
    shows = Show.objects.filter(show_date__gte=datetime.now()).order_by('show_date')
    return {'shows':shows}

@register.filter
def upcoming_show(show):
    if show.show_date > datetime.now():
        return True
    else:
        return False
