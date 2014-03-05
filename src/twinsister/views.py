from django.shortcuts import render
from kishore.models import Song

def home(request):
    try:
        song = Song.objects.get(title="Out of the Dark")
    except Song.DoesNotExist:
        song = None

    return render(request, "twinsister/home.html", {'song': song})
