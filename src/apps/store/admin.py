from django.contrib import admin

from apps.store.models import *


class IpnMessageAdmin(admin.ModelAdmin):
    readonly_fields = ('formatted',)
    date_hierarchy = 'timestamp'
    list_display = ('transaction_id', 'timestamp')

admin.site.register(PhysicalRelease)
admin.site.register(DigitalRelease)
admin.site.register(DigitalSong)
admin.site.register(IpnMessage, IpnMessageAdmin)
admin.site.register(Order)
