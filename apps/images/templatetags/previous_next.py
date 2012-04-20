from django import template
from django.core import urlresolvers

register = template.Library()

@register.filter
def previous_image(image, gallery):
    images = [x for x in gallery.images.order_by('order')]
    image_index = images.index(image)
    if image_index > 0:
        url = urlresolvers.reverse('image', kwargs={'gallery_id':gallery.id, 'image_id':images[image_index-1].id})
        return url
    else:
        return None

@register.filter
def next_image(image, gallery):
    images = [x for x in gallery.images.order_by('order')]
    image_index = images.index(image)
    if image_index < len(images) - 1:
        url = urlresolvers.reverse('image', kwargs={'gallery_id':gallery.id, 'image_id':images[image_index+1].id})
        return url
    else:
        return None

