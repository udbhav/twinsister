from django import template

from apps.music.models import Release

register = template.Library()

@register.filter
def get_tracklist(release):
    return release.songs.order_by('track_number')

@register.inclusion_tag('music/release_thumbnails.html')
def release_thumbnails():
    releases = Release.objects.filter(official=True).order_by('-pub_date')
    return {'releases': releases}
