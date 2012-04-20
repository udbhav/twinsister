from django.conf.urls.defaults import *
from django.views.generic import list_detail

from apps.images.models import *

galleries_info = {
    'queryset': Gallery.objects.filter(published=True),
    'paginate_by' : 25,
    'template_name' : 'images/galleries.html',
}

gallery_info = {
    'queryset': Gallery.objects.all(),
    'template_name': 'images/gallery.html',
    'template_object_name': 'gallery',
}

home_gallery_info = {
    'queryset': Gallery.objects.all(),
    'template_name': 'images/gallery_home.html',
    'template_object_name': 'gallery',
    'slug': 'photos',
}

flickr_photos_info = {
    'queryset': FlickrPhoto.objects.all(),
    'paginate_by' : 10,
    'template_name' : 'images/flickr_photos.html',
}

flickr_photo_info = {
    'queryset': FlickrPhoto.objects.all(),
    'template_name': 'data/data.html',
    'template_object_name': 'data',
    'slug_field': 'slug',
}

urlpatterns = patterns(
    '',
    (r'^$', list_detail.object_detail, home_gallery_info, 'galleries'),
    #(r'^$', list_detail.object_list, dict(galleries_info, page=1), 'galleries'),
    (r'^(?P<page>[0-9]+)/$', list_detail.object_list, galleries_info,),

    (r'^gallery/(?P<object_id>\d+)/$', list_detail.object_detail, gallery_info, 'gallery'),
    (r'^gallery/(?P<gallery_id>\d+)/(?P<image_id>\d+)/$', 'apps.images.views.image', {}, 'image'),

    #(r'^flickr/photo/(?P<slug>\d+)/$', list_detail.object_detail, flickr_photo_info, 'flickr_photo'),
)
