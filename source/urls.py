from django.conf.urls import *
from django.conf import settings
from django.contrib import admin
from django.views.generic import RedirectView, TemplateView

from kishore.urls import music as music_urls
from kishore.urls import store as store_urls
from kishore.urls import admin as admin_urls

from kishore.views import ReleaseList

urlpatterns = patterns(
    '',
    (r'^$', ReleaseList.as_view()),
    (r'^shows/$', TemplateView.as_view(template_name="shows.html"), {}, "shows"),

    (r'^music/', include(music_urls)),
    (r'^store/', include(store_urls)),
    (r'^manage/', include(admin_urls)),
    )

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(.*)$', 'django.views.static.serve', kwargs={'document_root': settings.MEDIA_ROOT}),
    )
