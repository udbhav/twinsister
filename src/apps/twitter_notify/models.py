from django.db.models.signals import post_save

from music.models import Data, Song, Release
from events.models import Show

def tweet_on_create(sender, instance, created, **kwargs):
    senders = (Data, Song, Release, Show)
    if sender in senders:
        if created:
            from views import post_to_twitter
            post_to_twitter(instance)

post_save.connect(tweet_on_create)
