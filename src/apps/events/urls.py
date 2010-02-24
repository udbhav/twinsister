from datetime import datetime
from datetime import timedelta

from django.conf.urls.defaults import *
from django.views.generic import list_detail
from django.contrib import databrowse

from apps.events.models import *

now = datetime.now()
difference = timedelta(hours=7)
date_result = now - difference

shows_info = {
    'queryset': Show.objects.filter(show_date__gte=date_result).order_by('show_date'),
    'paginate_by' : 25,
    'template_name' : 'events/shows.html',
}

show_info = {
    'queryset': Show.objects.all(),
    'template_name': 'data/data.html',
    'template_object_name': 'data',
    'slug_field': 'slug',
}

tour_info = {
    'queryset': Tour.objects.all(),
    'template_name': 'data/data.html',
    'template_object_name': 'data',
    'slug_field': 'slug',
}

urlpatterns = patterns(
    '',
    (r'^$', 'apps.events.views.shows', {}, 'shows'),
    (r'^tour/(?P<slug>[-\w]+)/$', list_detail.object_detail, tour_info, 'tour'),
    (r'^(?P<page>[0-9]+)/$', list_detail.object_list, shows_info),
    (r'^(?P<slug>[-\w]+)/$', list_detail.object_detail, show_info, 'show'),

    # This is for legacy show urls, added on 1/5/10, remove in a few months
    (r'^show/(?P<slug>[-\w]+)/$', 'django.views.generic.simple.redirect_to', {'url': '/shows/%(slug)s/'}),
)
