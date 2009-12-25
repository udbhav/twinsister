from django.db.models.signals import post_save
from django.conf import settings

from apps.data.models import Data
from apps.music.models import Song, Release
from apps.events.models import Show
from apps.images.models import Gallery

def tweet_on_create(sender, instance, created, **kwargs):
    senders = (Data, Song, Release, Show, Gallery)
    if sender in senders:
        if created and settings.TWITTER_USERNAME:
            from views import post_to_twitter
            post_to_twitter(instance)

post_save.connect(tweet_on_create)
