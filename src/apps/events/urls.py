from django.conf.urls.defaults import *
from django.views.generic import list_detail
from django.contrib import databrowse

from apps.events.models import *

shows_info = {
    'queryset': Show.objects.order_by('-show_date'),
    'paginate_by' : 25,
    'template_name' : 'events/shows.html',
}

show_info = {
    'queryset': Show.objects.all(),
    'template_name': 'data/data.html',
    'template_object_name': 'data',
    'slug_field': 'slug',
}

urlpatterns = patterns(
    '',
    (r'^$', list_detail.object_list, dict(shows_info, page=1), 'shows'),
    (r'^(?P<page>[0-9]+)/$', list_detail.object_list, shows_info),
    (r'^show/(?P<slug>[-\w]+)/$', list_detail.object_detail, show_info, 'show'),
)
