from django import template

from apps.images.models import FlickrPhoto

register = template.Library()

@register.filter
def sort_images(gallery):
    return gallery.images.order_by('order')

@register.filter
def grab_six(gallery):
    return gallery.images.order_by('order')[:6]

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

@register.inclusion_tag('images/recent_flickr.html')
def recent_flickr():
    photos = FlickrPhoto.objects.all()[:6]
    return {'photos':photos}

@register.filter
def get_primary_image(musicdata):
    try:
        return musicdata.artwork.images.order_by('order')[0]
    except IndexError:
        return None

