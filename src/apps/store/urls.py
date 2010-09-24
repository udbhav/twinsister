from django.conf.urls.defaults import *

urlpatterns = patterns(
    '',
    (r'^ipn/$', 'apps.store.views.ipn', {}, 'store_ipn'),
    (r'^success/$', 'apps.store.views.success', {}, 'store_success'),
)
