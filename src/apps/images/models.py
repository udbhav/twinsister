from datetime import datetime

from django.db import models
from django.core import urlresolvers

from apps.people.models import Person

class Image(models.Model):
	title = models.CharField(max_length=50)
	photo = models.ImageField(upload_to='uploads/images')
	caption = models.TextField(null=True, blank=True)
	credit = models.ManyToManyField(Person, null=True, blank=True)
	pub_date = models.DateTimeField('date published', default=datetime.now)
        order = models.IntegerField(default=1)

	def __unicode__(self):
		return self.title

class Gallery(models.Model):
	title = models.CharField(max_length=70)
	description = models.TextField(null=True, blank=True)
	images = models.ManyToManyField(Image)
	pub_date = models.DateTimeField('date published', default=datetime.now)

	def __unicode__(self):
		return self.title
        def get_absolute_url(self):
                url = urlresolvers.reverse('gallery', kwargs={'object_id':self.id})
                return url
	class Meta:
		verbose_name_plural = 'Galleries'
