from django.contrib import admin

from apps.events.models import Show, Venue
from apps.music.admin import PrepopulatedAdmin

class ShowAdmin(PrepopulatedAdmin):
    list_display = ('name', 'show_date')
    filter_horizontal = ('bands',)

admin.site.register(Show, ShowAdmin)
admin.site.register(Venue)
