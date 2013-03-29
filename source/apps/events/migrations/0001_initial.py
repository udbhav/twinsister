
from south.db import db
from django.db import models
from apps.events.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Venue'
        db.create_table('events_venue', (
            ('id', orm['events.Venue:id']),
            ('name', orm['events.Venue:name']),
            ('address', orm['events.Venue:address']),
        ))
        db.send_create_signal('events', ['Venue'])
        
        # Adding model 'Tour'
        db.create_table('events_tour', (
            ('data_ptr', orm['events.Tour:data_ptr']),
        ))
        db.send_create_signal('events', ['Tour'])
        
        # Adding model 'Show'
        db.create_table('events_show', (
            ('data_ptr', orm['events.Show:data_ptr']),
            ('venue', orm['events.Show:venue']),
            ('show_date', orm['events.Show:show_date']),
            ('cost', orm['events.Show:cost']),
        ))
        db.send_create_signal('events', ['Show'])
        
        # Adding ManyToManyField 'Tour.shows'
        db.create_table('events_tour_shows', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tour', models.ForeignKey(orm.Tour, null=False)),
            ('show', models.ForeignKey(orm.Show, null=False))
        ))
        
        # Adding ManyToManyField 'Show.bands'
        db.create_table('events_show_bands', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('show', models.ForeignKey(orm.Show, null=False)),
            ('band', models.ForeignKey(orm['people.Band'], null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Venue'
        db.delete_table('events_venue')
        
        # Deleting model 'Tour'
        db.delete_table('events_tour')
        
        # Deleting model 'Show'
        db.delete_table('events_show')
        
        # Dropping ManyToManyField 'Tour.shows'
        db.delete_table('events_tour_shows')
        
        # Dropping ManyToManyField 'Show.bands'
        db.delete_table('events_show_bands')
        
    
    
    models = {
        'data.data': {
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'header_image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.HeaderImage']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'posted_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Person']"}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 2, 23, 20, 52, 22, 467243)'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'data.headerimage': {
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'events.show': {
            'bands': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['people.Band']", 'null': 'True', 'blank': 'True'}),
            'cost': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'data_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['data.Data']", 'unique': 'True', 'primary_key': 'True'}),
            'show_date': ('django.db.models.fields.DateTimeField', [], {}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Venue']"})
        },
        'events.tour': {
            'data_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['data.Data']", 'unique': 'True', 'primary_key': 'True'}),
            'shows': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['events.Show']"})
        },
        'events.venue': {
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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
    
    complete_apps = ['events']
