from datetime import datetime

from django.db import models
from django.db.models.signals import pre_save
from django.core import urlresolvers
from django.conf import settings
import flickrapi
from imagekit.models import ImageModel

from apps.people.models import Person
from apps.data.models import Data

class Image(ImageModel):
    title = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='uploads/images')
    caption = models.TextField(null=True, blank=True)
    credit = models.ManyToManyField(Person, null=True, blank=True)
    pub_date = models.DateTimeField('date published', default=datetime.now)
    order = models.IntegerField(default=1)

    def __unicode__(self):
        return self.title

    class IKOptions:
        spec_module = 'apps.images.specs'
        image_field = 'photo'

class Gallery(Data):
    images = models.ManyToManyField(Image)

    def get_absolute_url(self):
        url = urlresolvers.reverse('gallery', kwargs={'object_id':self.id})
        return url

    def get_template(self):
        return 'images/gallery_content.html'

    class Meta:
        verbose_name_plural = 'Galleries'

class FlickrUser(models.Model):
    flickr_username = models.CharField(max_length=20)
    flickr_id = models.CharField(max_length=30, editable=False)
    person = models.ForeignKey(Person)

    def __unicode__(self):
        return self.flickr_username
    def get_absolute_url(self):
        return 'http://flickr.com/photos/%s/' % self.flickr_id

class FlickrTag(models.Model):
    tag = models.CharField(max_length=20)

    def __unicode__(self):
        return self.tag
    def flickr_format(self):
        return self.tag.replace(' ', '').lower()

class FlickrPhoto(models.Model):
    user = models.ForeignKey(FlickrUser)
    title = models.CharField(max_length=100, blank=True)
    farm = models.IntegerField()
    server = models.IntegerField()
    photo_id = models.CharField(max_length=50)
    secret = models.CharField(max_length=50)
    upload_date = models.DateField()

    def __unicode__(self):
        return '%s: %s' % (self.photo_id, self.title)
    def get_large_photo(self):
        return 'http://farm%i.static.flickr.com/%i/%s_%s.jpg' % (self.farm, self.server, self.photo_id, self.secret)
    def get_small_square(self):
        return 'http://farm%i.static.flickr.com/%i/%s_%s_s.jpg' % (self.farm, self.server, self.photo_id, self.secret)
    def get_flickr_page(self):
        return 'http://flickr.com/photos/%s/%s/' % (self.user.flickr_id, self.photo_id)
    class Meta:
        ordering = ('-upload_date',)

flickr = flickrapi.FlickrAPI(settings.FLICKR_API_KEY)

def sync_flickr_photos():
    for user in FlickrUser.objects.all():
        dupe = False
        current_page = 1
        desired_tags = set([x.flickr_format() for x in FlickrTag.objects.all()])
        while (not dupe):
            photos = flickr.people_getPublicPhotos(user_id=user.flickr_id, extras='date_upload,tags', page=current_page).find('photos')
            current_page += 1

            for photo in photos:
                tags = photo.get('tags').split(' ')
                if desired_tags.intersection(tags):
                    try:
                        row = FlickrPhoto.objects.get(slug=photo.get("id"), secret=photo.get("secret"))
                    except FlickrPhoto.DoesNotExist:
                        FlickrPhoto.objects.create(
                            user = user,
                            name = photo.get("title")[:100],
                            farm = int(photo.get("farm")),
                            server = int(photo.get("server")),
                            slug = int(photo.get("id")),
                            secret = photo.get("secret"),
                            pub_date = datetime.fromtimestamp(int(photo.get("dateupload"))),
                            posted_by = user.person,
                            )
                    else:
                        dupe = True
                        break

            if photos.get('page') == photos.get('pages'):
                break
                                                
def grab_nsid(sender, instance, *args, **kwargs):
    if not instance.flickr_id:
        instance.flickr_id = flickr.people_findByUsername(username=instance.flickr_username).find('user').get('nsid')
                
pre_save.connect(grab_nsid, sender=FlickrUser)
