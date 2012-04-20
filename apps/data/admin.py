from django.contrib import admin

from apps.data.models import *

def make_published(modeladmin, request, queryset):
    queryset.update(published=True)
make_published.short_description = "Mark selected as published"

class WYMEditorAdmin(admin.ModelAdmin):
        class Media:
                css = {
                        "screen": ("/media/css/wymeditor.css",)
                        }
                js = (
                        'js/jquery-1.3.2.min.js',
                        '/media/wymeditor/jquery.wymeditor.pack.js',
                        '/media/js/add_wym.js',
                        )

class PrepopulatedAdmin(WYMEditorAdmin):
        prepopulated_fields = {'slug': ('name',)}
        list_display = ('name', 'pub_date', 'published')
        search_fields = ('name',)
        actions = [make_published]

admin.site.register(Data, PrepopulatedAdmin)
admin.site.register(HeaderImage)
