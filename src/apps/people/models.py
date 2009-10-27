from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField(verify_exists=True, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ('name',)
	verbose_name_plural = 'People'
    def __unicode__(self):
        return self.name
    
class Band(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField(verify_exists=True, null=True, blank=True)
    members = models.ManyToManyField(Person, null=True, blank=True)
    class Meta:
        ordering = ('name',)
    def __unicode__(self):
        return self.name
