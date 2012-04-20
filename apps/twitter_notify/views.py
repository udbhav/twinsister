from urllib2 import HTTPError
import twitter

from django.conf import settings
from django.contrib.sites.models import Site

from bitly import shorten

site = Site.objects.get_current()
api = twitter.Api(username=settings.TWITTER_USERNAME, password=settings.TWITTER_PASSWORD)

def post_to_twitter(data):
    url = shorten('http://%s%s' % (site.domain, data.get_absolute_url()))
    post = '%s: %s' % (data.get_human_class_type(), data.name)
    if len(post) >= 130:
        post = post[:127] + '...'

    post_string = '%s %s' % (post, url)
    try:
        api.PostUpdate(post_string[:140])
    except HTTPError:
        pass
