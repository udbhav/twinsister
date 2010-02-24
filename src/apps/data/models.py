from datetime import datetime

from django.db import models
from django.core import urlresolvers
from django.db.models.signals import post_delete
from imagekit.models import ImageModel
from apps.data.listeners import delete_subclasses
from apps.people.models import Person

class HeaderImage(ImageModel):
    image = models.ImageField(upload_to='uploads/images', blank=True, null=True)
    caption = models.TextField(blank=True)

    def __unicode__(self):
        return self.image.name

    class IKOptions:
        spec_module = 'apps.data.specs'
        cache_dir = 'uploads/images'
        image_field = 'image'

class Data(models.Model):
    """
    An all-purpose container for all content on the site

    # Create some Data and check out the methods!
    >>> from apps.people.models import Person
    >>> person = Person.objects.create(name="Udbhav Gupta")
    >>> d = Data.objects.create(name="Kickin' out the Jamz", slug="kickin-out-the-jamz", posted_by=person)
    >>> d
    <Data: Kickin' out the Jamz>
    >>> d.get_class_type()
    'Entry'
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    posted_by = models.ForeignKey(Person)
    pub_date = models.DateTimeField('date published', default=datetime.now())
    description = models.TextField(blank=True)
    header_image = models.ForeignKey(HeaderImage, blank=True, null=True)
    published = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    def get_class_type(self):
        subclasses = ('musicdata', 'gallery', 'show', 'imagebase', 'tour')
        for subclass in subclasses:
            if hasattr(self, subclass):
                return subclass
        return None

    def get_absolute_url(self):
        subclass = self.get_class_type()
        if subclass:
            return getattr(self, subclass).get_absolute_url()
        else:
            return urlresolvers.reverse('entry', kwargs={'slug':self.slug})

    def get_human_class_type(self):
        classes = {
            'gallery': 'Gallery',
            'show': 'Show',
            'flickrphoto': 'Gallery',
            'tour': 'Tour',
        }

        subclass = self.get_class_type()

        if subclass == 'musicdata' or subclass == 'imagebase':
            return getattr(self, subclass).get_human_class_type()
        else:
            return classes.get(subclass, 'Entry')

    def get_template(self):
        subclass = self.get_class_type()
        if subclass:
            return getattr(self, subclass).get_template()
        else:
            return None

    class Meta:
        verbose_name_plural = 'Entries'
        verbose_name = 'Entry'
        ordering = ('-pub_date',)

post_delete.connect(delete_subclasses)
