
from south.db import db
from django.db import models
from apps.people.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Person'
        db.create_table('people_person', (
            ('id', orm['people.Person:id']),
            ('name', orm['people.Person:name']),
            ('url', orm['people.Person:url']),
            ('email', orm['people.Person:email']),
        ))
        db.send_create_signal('people', ['Person'])
        
        # Adding model 'Band'
        db.create_table('people_band', (
            ('id', orm['people.Band:id']),
            ('name', orm['people.Band:name']),
            ('url', orm['people.Band:url']),
        ))
        db.send_create_signal('people', ['Band'])
        
        # Adding ManyToManyField 'Band.members'
        db.create_table('people_band_members', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('band', models.ForeignKey(orm.Band, null=False)),
            ('person', models.ForeignKey(orm.Person, null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Person'
        db.delete_table('people_person')
        
        # Deleting model 'Band'
        db.delete_table('people_band')
        
        # Dropping ManyToManyField 'Band.members'
        db.delete_table('people_band_members')
        
    
    
    models = {
        'people.band': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['people.Person']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'people.person': {
            'email': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }
    
    complete_apps = ['people']
