from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required

from apps.music.models import Release
from apps.store.models import Order
from apps.store.views import BuyReleaseView, StoreAdminView, OrderDetailView, CompletedOrdersView

urlpatterns = patterns(
    '',
    (r'^buy/(?P<slug>[-\w]+)/$', BuyReleaseView.as_view(), {}, 'store_buy'),
    (r'^download/(?P<download_key>\w+)/$', 'apps.store.views.download', {}, 'store_download'),
    (r'^download/process/(?P<download_key>\w+)/(?P<product_id>\d+)/$', 'apps.store.views.process_download', {}, 'store_process_download'),
    (r'^ipn/$', 'apps.store.views.ipn', {}, 'store_ipn'),
    (r'^success/$', 'apps.store.views.success', {}, 'store_success'),
    (r'^admin/$', login_required(StoreAdminView.as_view()), {}, 'store_admin'),
    (r'^admin/completed/$', login_required(CompletedOrdersView.as_view()), {}, 'completed_orders'),
    (r'^admin/order/(?P<pk>\d+)/$', login_required(OrderDetailView.as_view()), {}, 'order_detail'),
    (r'^admin/ship-order/$', 'apps.store.views.ship_order', {}, 'ship_order'),
)
