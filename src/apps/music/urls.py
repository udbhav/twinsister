from django.conf.urls.defaults import *
from django.views.generic import list_detail

from apps.music.models import *

songs_info = {
    'queryset': Song.objects.order_by('-official', '-pub_date'),
    'paginate_by' : 25,
    'template_name' : 'music/songs.html',
}

song_info = {
    'queryset': Song.objects.all(),
    'template_name': 'data/data.html',
    'template_object_name': 'data',
    'slug_field': 'slug',
}

releases_info = {
    'queryset': Release.objects.order_by('-official', '-pub_date'),
    'paginate_by' : 25,
    'template_name' : 'music/releases.html',
}

release_info = {
    'queryset': Release.objects.order_by(),
    'template_name': 'data/data.html',
    'template_object_name': 'data',
    'slug_field': 'slug',
}

urlpatterns = patterns(
    '',
    (r'^songs/$', list_detail.object_list, dict(songs_info, page=1), 'songs'),
    (r'^songs/(?P<page>[0-9]+)/$', list_detail.object_list, songs_info),
    (r'^song/(?P<slug>[-\w]+)/$', list_detail.object_detail, song_info, 'song'),
    (r'^releases/$', list_detail.object_list, dict(releases_info, page=1), 'releases'),
    (r'^releases/(?P<page>[0-9]+)/$', list_detail.object_list, releases_info),
    (r'^release/(?P<slug>[-\w]+)/$', list_detail.object_detail, release_info, 'release'),
)
