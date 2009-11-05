from django.contrib import admin

from apps.images.models import *
from apps.data.admin import *

admin.site.register(Gallery, PrepopulatedAdmin)
admin.site.register(Image)
admin.site.register(FlickrUser)
admin.site.register(FlickrPhoto)
admin.site.register(FlickrTag)
