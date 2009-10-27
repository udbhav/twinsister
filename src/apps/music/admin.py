from django.contrib import admin

from apps.music.models import *

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
admin.site.register(Data, PrepopulatedAdmin)
