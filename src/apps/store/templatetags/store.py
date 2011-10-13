from urllib import urlencode
import locale

from django import template
from django.conf import settings
from django.core import urlresolvers

from apps.store.models import PhysicalRelease

register = template.Library()

@register.filter
def get_paypal_link(product):
    paypal_dict = {
        "cmd": "_xclick",
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": product.cost,
        "item_name": product.__unicode__(),
        "notify_url": settings.PAYPAL_NOTIFY_URL,
        "return": settings.PAYPAL_RETURN_URL,
        "cancel_return": settings.PAYPAL_CANCEL_URL,
        "item_number": product.id,
        }

    if product.__class__ == PhysicalRelease:
        paypal_dict['no_shipping'] = 2
        paypal_dict['undefined_quantity'] = 1
    else:
        paypal_dict['no_shipping'] = 1

    return settings.PAYPAL_SUBMIT_URL + urlencode(paypal_dict)

@register.filter
def currency(value):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    return locale.currency(float(value))


@register.filter
def get_buy_link(release):
    if release.digitalrelease_set.all() or release.physicalrelease_set.all():
        url = urlresolvers.reverse('store_buy', kwargs = {'slug': release.slug})
        return url
    else:
        return None
