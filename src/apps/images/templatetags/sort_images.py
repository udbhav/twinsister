from django import template

register = template.Library()

@register.filter
def sort_images(gallery):
    return gallery.images.order_by('order')


@register.filter
def grab_six(gallery):
    return gallery.images.order_by('order')[:6]
