from django.contrib import admin

from apps.music.models import *
from apps.data.admin import *

class CreditInline(admin.TabularInline):
        model = Credit
        extra = 5

class SongAdmin(PrepopulatedAdmin):
        inlines = [CreditInline]

class ReleaseAdmin(PrepopulatedAdmin):
        filter_horizontal = ('songs',)

admin.site.register(Release, PrepopulatedAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(Archive)
admin.site.register(Stem)
