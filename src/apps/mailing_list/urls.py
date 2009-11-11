from django.conf.urls.defaults import *

urlpatterns = patterns(
    '',
    (r'^subscribe/$', 'apps.mailing_list.views.subscribe', {}, 'subscribe'),
    (r'^subscription-complete/$', 'django.views.generic.simple.direct_to_template', {'template':'mailing_list/subscription_complete.html'}, 'subscription_complete'),
)
