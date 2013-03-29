from django.contrib import admin

from apps.images.models import *
from apps.data.admin import *

class GalleryAdmin(PrepopulatedAdmin):
    filter_horizontal = ('images',)

admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Image)
admin.site.register(FlickrUser)
admin.site.register(FlickrPhoto)
admin.site.register(FlickrTag)
