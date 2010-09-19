from django.contrib import admin

from apps.store.models import *

admin.site.register(PhysicalRelease)
admin.site.register(DigitalRelease)
admin.site.register(DigitalSong)
