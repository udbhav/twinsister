from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.views.generic import list_detail

from feeds import Entries

from apps.data.models import *
from apps.music.models import *
from apps.events.models import *
from apps.images.models import *
from apps.people.models import *

admin.autodiscover()

feeds = {
    'entries': Entries,
    }

urlpatterns = patterns(
    '',
    (r'^music/', include('apps.music.urls')),
    (r'^images/', include('apps.images.urls')),
    (r'^shows/', include('apps.events.urls')),

    # This is for legacy links to shows and etc.  Added 1/5/10, remove after a 4-5 months
    (r'^events(?P<argument>.*)/$', 'django.views.generic.simple.redirect_to', {'url': '/shows%(argument)s/'}),

    (r'^mailing-list/', include('apps.mailing_list.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    # (r'^search/', include('haystack.urls')),
    (r'^faq/$', 'django.views.generic.simple.direct_to_template', {'template':'faq.html'}),
    (r'^admin/filebrowser/', include('filebrowser.urls')),
    (r'^admin/(.*)', admin.site.root),
    (r'^', include('apps.data.urls')),
    )

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(.*)$', 'django.views.static.serve', kwargs={'document_root': settings.MEDIA_ROOT}),
    )
