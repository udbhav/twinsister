from django.contrib import admin

from apps.images.models import *

class GalleryAdmin(admin.ModelAdmin):
	class Media:
		js = ('/site_media/tiny_mce/tiny_mce.js',
		      '/site_media/tiny_mce/textarea.js',)

admin.site.register(Gallery)
admin.site.register(Image)
