from django.conf.urls.defaults import *
from django.views.generic import DetailView

from apps.music.models import Release
from apps.store.models import Order
from apps.store.views import BuyReleaseView

urlpatterns = patterns(
    '',
    (r'^buy/(?P<slug>[-\w]+)/$', BuyReleaseView.as_view(), {}, 'store_buy'),
    (r'^download/(?P<download_key>\w+)/$', 'apps.store.views.download', {}, 'store_download'),
    (r'^download/process/(?P<download_key>\w+)/(?P<product_id>\d+)/$', 'apps.store.views.process_download', {}, 'store_process_download'),
    (r'^ipn/$', 'apps.store.views.ipn', {}, 'store_ipn'),
    (r'^success/$', 'apps.store.views.success', {}, 'store_success'),
#    (r'^admin/$', list_detail.object_list, dict(order_info, page=1), 'store_admin'),
#    (r'^admin/(?P<page>[0-9]+/$', list_detail.object_detail, order_info),
)
