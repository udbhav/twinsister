from django.conf.urls import *
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import urls as auth_urls
from django.views.generic import RedirectView

from kishore.urls import music as music_urls
from kishore.urls import store as store_urls
from kishore.views import ReleaseIndex

admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^$', ReleaseIndex.as_view()),
    (r'^music/', include(music_urls)),
    (r'^store/', include(store_urls)),

    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/$', RedirectView.as_view(url='/accounts/login/'), {}),
    (r'^accounts/', include(auth_urls)),
    )

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(.*)$', 'django.views.static.serve', kwargs={'document_root': settings.MEDIA_ROOT}),
    )
