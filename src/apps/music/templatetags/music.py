from django import template

register = template.Library()

@register.filter
def get_tracklist(release):
    return release.songs.order_by('track_number')
