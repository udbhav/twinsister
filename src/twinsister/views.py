from django.shortcuts import render
from django.conf import settings
from django.views.decorators.cache import cache_page
from kishore.models import Song, Release

@cache_page
def home(request):
    try:
        song = Song.objects.get(title="Out of the Dark")
    except Song.DoesNotExist:
        song = None

    return render(request, "twinsister/home.html", {'song': song})

def test(request):
    song = Song.objects.all()[0]
    return render(request, "twinsister/test.html", {'song': song})
