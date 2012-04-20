from django.contrib import admin

from apps.events.models import Show, Venue, Tour
from apps.data.admin import PrepopulatedAdmin, make_published

class ShowAdmin(PrepopulatedAdmin):
    list_display = ('name', 'show_date')
    filter_horizontal = ('bands',)
    actions = [make_published]

admin.site.register(Show, ShowAdmin)
admin.site.register(Venue)
admin.site.register(Tour, PrepopulatedAdmin)
