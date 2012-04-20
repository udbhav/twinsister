from django.db import models
from django import forms

class Subscriber(models.Model):
    email = models.EmailField(unique=True)

    def __unicode__(self):
        return self.email

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
