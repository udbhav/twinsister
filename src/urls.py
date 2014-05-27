from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import urls as auth_urls
from django.views.generic import list_detail, RedirectView

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
    (r'^store/', include('apps.store.urls')),

    # This is for legacy links to shows and etc.  Added 1/5/10, remove after a 4-5 months
    (r'^events(?P<argument>.*)/$', 'django.views.generic.simple.redirect_to', {'url': '/shows%(argument)s/'}),

    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    (r'^search/', include('haystack.urls')),
    (r'^contact/$', 'django.views.generic.simple.direct_to_template', {'template':'contact.html'}),
    (r'^faq/$', 'django.views.generic.simple.direct_to_template', {'template':'faq.html'}),
    #(r'^admin/filebrowser/', include('filebrowser.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/$', RedirectView.as_view(url='/accounts/login/'), {}),
    (r'^accounts/', include(auth_urls)),
    (r'^', include('apps.data.urls')),
    )

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(.*)$', 'django.views.static.serve', kwargs={'document_root': settings.MEDIA_ROOT}),
    )
