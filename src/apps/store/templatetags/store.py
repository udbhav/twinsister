from urllib import urlencode

from django import template
from django.conf import settings

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
        "return_url": settings.PAYPAL_RETURN_URL,
        "cancel_return": settings.PAYPAL_CANCEL_URL,
        "item_number": product.id,
        }

    if product.__class__ == PhysicalRelease:
        paypal_dict['no_shipping'] = 0
        paypal_dict['undefined_quantity'] = 1

    return settings.PAYPAL_SUBMIT_URL + '?' + urlencode(paypal_dict)
