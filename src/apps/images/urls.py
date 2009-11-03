from django.conf.urls.defaults import *
from django.views.generic import list_detail

from apps.images.models import *

galleries_info = {
    'queryset': Gallery.objects.all(),
    'paginate_by' : 25,
    'template_name' : 'images/galleries.html',
}

gallery_info = {
    'queryset': Gallery.objects.all(),
    'template_name': 'images/gallery.html',
    'template_object_name': 'gallery',
}

flickr_photos_info = {
    'queryset': FlickrPhoto.objects.all(),
    'paginate_by' : 10,
    'template_name' : 'images/flickr_photos.html',
}

urlpatterns = patterns(
    '',
    (r'^$', list_detail.object_list, dict(galleries_info, page=1), 'galleries'),
    (r'^(?P<page>[0-9]+)/$', list_detail.object_list, galleries_info,),
    (r'^flickr/$', list_detail.object_list, dict(flickr_photos_info, page=1), 'flickr_photos'),
    (r'^flickr/(?P<page>[0-9]+)/$', list_detail.object_list, flickr_photos_info,),

    (r'^gallery/(?P<object_id>\d+)/$', list_detail.object_detail, gallery_info, 'gallery'),
    (r'^(?P<gallery_id>\d+)/(?P<image_id>\d+)/$', 'apps.images.views.image', {}, 'image'),
)
