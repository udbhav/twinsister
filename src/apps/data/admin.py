from django.contrib import admin

from apps.data.models import *

class WYMEditorAdmin(admin.ModelAdmin):
        class Media:
                css = {
                        "screen": ("css/wymeditor.css",)
                        }
                js = (
                        'js/jquery-1.3.2.min.js',
                        'wymeditor/jquery.wymeditor.pack.js',
                        'js/add_wym.js',
                        )

class PrepopulatedAdmin(WYMEditorAdmin):
        prepopulated_fields = {'slug': ('name',)}
        list_display = ('name', 'pub_date', 'published')
        search_fields = ('name',)

admin.site.register(Data, PrepopulatedAdmin)
admin.site.register(HeaderImage)
