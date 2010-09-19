from django.conf.urls.defaults import *

urlpatterns = patterns(
    '',
    (r'^success/$', 'apps.store.views.success', {}, 'store_success'),
)
