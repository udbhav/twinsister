from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin, databrowse
from django.views.generic import list_detail

from feeds import Entries
from apps.music.models import *
from apps.events.models import *
from apps.images.models import *
from apps.people.models import *

# databrowse.site.register(Song)
# databrowse.site.register(Release)
# databrowse.site.register(Image)
# databrowse.site.register(Gallery)
# databrowse.site.register(Person)
# databrowse.site.register(Band)
# databrowse.site.register(Show)

admin.autodiscover()

feeds = {
    'entries': Entries,
    }

urlpatterns = patterns(
    '',
    (r'^images/', include('apps.images.urls')),
    (r'^events/', include('apps.events.urls')),
    (r'^mailing-list/', include('apps.mailing_list.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    (r'^browse/(.*)', databrowse.site.root),
    (r'^search/', include('haystack.urls')),
    (r'^faq/$', 'django.views.generic.simple.direct_to_template', {'template':'faq.html'}),
    (r'^admin/filebrowser/', include('filebrowser.urls')),
    (r'^admin/(.*)', admin.site.root),
    (r'^', include('apps.music.urls')),
    )

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(.*)$', 'django.views.static.serve', kwargs={'document_root': settings.MEDIA_ROOT}),
    )
