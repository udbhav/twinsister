from django.conf.urls.defaults import *
from django.views.generic import list_detail

from apps.data.models import Data
from apps.music.models import Release

data_list_info = {
    'queryset': Data.objects.filter(published=True).filter(show=None).filter(imagebase=None).order_by('-pub_date'),
    'paginate_by' : 15,
    'template_name' : 'data/data_list.html',
}

data_info = {
    'queryset': Data.objects.all(),
    'template_name': 'data/data.html',
    'template_object_name': 'data',
    'slug_field': 'slug',
}

home_info = {
    'queryset': Release.objects.filter(official=True).order_by('-pub_date'),
    'template_name': 'home.html',
}

urlpatterns = patterns(
    '',
    (r'^$', 'home.splash_page'),
    (r'^entry/(?P<slug>[-\w]+)/$', list_detail.object_detail, data_info, 'entry'),
    (r'entries-by-person/(?P<person_id>\d+)/$', 'apps.data.views.entries_by_person', {}, 'entries_by_person'),
    (r'entries-by-person/(?P<person_id>\d+)/(?P<page>[0-9]+)/$', 'apps.data.views.entries_by_person', {}, 'entries_by_person_paginated'),
    (r'^(?P<page>[0-9]+)/$', list_detail.object_list, data_list_info, 'entries_by_page'),
)
