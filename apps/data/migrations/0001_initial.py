
from south.db import db
from django.db import models
from apps.data.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'HeaderImage'
        db.create_table('data_headerimage', (
            ('id', orm['data.HeaderImage:id']),
            ('image', orm['data.HeaderImage:image']),
            ('caption', orm['data.HeaderImage:caption']),
        ))
        db.send_create_signal('data', ['HeaderImage'])
        
        # Adding model 'Data'
        db.create_table('data_data', (
            ('id', orm['data.Data:id']),
            ('name', orm['data.Data:name']),
            ('slug', orm['data.Data:slug']),
            ('posted_by', orm['data.Data:posted_by']),
            ('pub_date', orm['data.Data:pub_date']),
            ('description', orm['data.Data:description']),
            ('header_image', orm['data.Data:header_image']),
            ('published', orm['data.Data:published']),
        ))
        db.send_create_signal('data', ['Data'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'HeaderImage'
        db.delete_table('data_headerimage')
        
        # Deleting model 'Data'
        db.delete_table('data_data')
        
    
    
    models = {
        'data.data': {
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'header_image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.HeaderImage']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'posted_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Person']"}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 2, 23, 20, 51, 53, 935754)'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'data.headerimage': {
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'people.person': {
            'email': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }
    
    complete_apps = ['data']
