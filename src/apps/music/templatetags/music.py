from django import template

from apps.music.models import Release

register = template.Library()

@register.filter
def get_tracklist(release):
    return release.songs.order_by('track_number')
