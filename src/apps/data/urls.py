from django.conf.urls.defaults import *
from django.views.generic import list_detail

from apps.data.models import Data
from apps.music.models import Release

data_list_info = {
    'queryset': Data.objects.filter(published=True).order_by('-pub_date'),
    'paginate_by' : 15,
    'template_name' : 'music/data_list.html',
}

data_info = {
    'queryset': Data.objects.all(),
    'template_name': 'music/data.html',
    'template_object_name': 'data',
    'slug_field': 'slug',
}

home_info = dict(
    data_list_info,
    page = 1,
    template_name = 'home.html',
    )

try:
    featured_release = Release.objects.filter(official=True).order_by('-pub_date')[0]
except IndexError:
    pass
else:
    home_info['extra_context'] = {
        'featured_release': featured_release,
}

urlpatterns = patterns(
    '',
    (r'^$', list_detail.object_list, home_info),
    (r'^(?P<page>[0-9]+)/$', list_detail.object_list, data_list_info),
    (r'^entry/(?P<slug>[-\w]+)/$', list_detail.object_detail, data_info, 'entry'),
)
