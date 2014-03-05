from django.conf.urls import patterns, include, url

from kishore.urls import music as music_urls
from kishore.urls import store as store_urls
from kishore.urls import admin as admin_urls
from kishore.urls import search as search_urls

from kishore.views import ReleaseList

urlpatterns = patterns(
    '',
    (r'^$', 'twinsister.views.home'),

    (r'^music/', include(music_urls)),
    (r'^store/', include(store_urls)),
    (r'^manage/', include(admin_urls)),
    (r'^search/', include(search_urls)),
    ('^accounts/', include('django.contrib.auth.urls')),
)
