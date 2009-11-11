from django.contrib import admin

from apps.people.models import Person, Band

admin.site.register(Person)
admin.site.register(Band)
