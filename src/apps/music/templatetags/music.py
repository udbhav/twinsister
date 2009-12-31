from django import template

from apps.music.models import Release

register = template.Library()

@register.filter
def get_tracklist(release):
    return release.songs.order_by('track_number')

@register.inclusion_tag('music/featured_release_thumbnail.html')
def featured_release_thumbnail():
    try:
        featured_release = Release.objects.filter(official=True).order_by('-pub_date')[0]
    except IndexError:
        featured_release = None
    
    return {'featured_release': featured_release}
    
