from django_extensions.management.jobs import DailyJob

from apps.images.models import sync_flickr_photos

class Job(DailyJob):
    help = "Sync photos from Flickr"

    def execute(self):
        print "Syncing Flickr Photos"
        sync_flickr_photos()
        print "Flickr Sync complete!"
        

