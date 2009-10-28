from django.db import models

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
    header_image = models.ImageField(upload_to='uploads/images', blank=True, null=True)
    published = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        from apps.music.models import Song, Release
        from apps.events.models import Show
        url = None
        try:
            self.song
            url = self.song.get_absolute_url()
        except Song.DoesNotExist:
            pass
        try:
            self.release
            url = self.release.get_absolute_url()
        except Release.DoesNotExist:
            pass
        try:
            self.show
            url = self.show.get_absolute_url()
        except Show.DoesNotExist:
            pass
        if not url:
            url = urlresolvers.reverse('entry', kwargs={'slug':self.slug})
        return url

    def get_class_type(self):
        from apps.music.models import Song, Release
        from apps.events.models import Show
        class_type = None
        try:
            self.song
            class_type = 'Song'
        except Song.DoesNotExist:
            pass
        try:
            self.release
            class_type = 'Release'
        except Release.DoesNotExist:
            pass
        try:
            self.show
            class_type = 'Show'
        except Show.DoesNotExist:
            pass
        if not class_type:
            class_type = 'Entry'
        return class_type

    class Meta:
        verbose_name_plural = 'Entries'
        verbose_name = 'Entry'
