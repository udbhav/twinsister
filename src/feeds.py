from django.contrib.syndication.feeds import Feed

from apps.music.models import Data

class Entries(Feed):
	title = "Ideas and etc. from twinsistermusic.com"
	link = "http://twinsistermusic.com/"
	description = "Ideas and etc. from Twin Sister"
	
	def items(self):
		return Data.objects.order_by('-pub_date')
	def item_pubdate(self, item):
		return item.pub_date

