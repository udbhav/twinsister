# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Cart'
        db.create_table('kishore_carts', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 3, 20, 0, 0))),
        ))
        db.send_create_signal('kishore', ['Cart'])


    def backwards(self, orm):
        # Deleting model 'Cart'
        db.delete_table('kishore_carts')


    models = {
        'kishore.artist': {
            'Meta': {'object_name': 'Artist', 'db_table': "'kishore_artists'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'kishore.cart': {
            'Meta': {'object_name': 'Cart', 'db_table': "'kishore_carts'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 3, 20, 0, 0)'})
        },
        'kishore.digitalrelease': {
            'Meta': {'object_name': 'DigitalRelease', 'db_table': "'kishore_digitalreleases'", '_ormbases': ['kishore.Product']},
            'audio_format': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'product_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['kishore.Product']", 'unique': 'True', 'primary_key': 'True'}),
            'release': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['kishore.Release']"}),
            'zipfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'kishore.digitalsong': {
            'Meta': {'object_name': 'DigitalSong', 'db_table': "'kishore_digitalsongs'", '_ormbases': ['kishore.Product']},
            u'product_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['kishore.Product']", 'unique': 'True', 'primary_key': 'True'}),
            'song': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['kishore.Song']", 'unique': 'True'})
        },
        'kishore.image': {
            'Meta': {'object_name': 'Image', 'db_table': "'kishore_images'"},
            'credit': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'kishore.merch': {
            'Meta': {'object_name': 'Merch', '_ormbases': ['kishore.Product']},
            u'product_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['kishore.Product']", 'unique': 'True', 'primary_key': 'True'}),
            'variants': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['kishore.MerchVariant']", 'symmetrical': 'False'})
        },
        'kishore.merchvariant': {
            'Meta': {'object_name': 'MerchVariant', 'db_table': "'kishore_merchvariants'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['kishore.Image']", 'symmetrical': 'False'}),
            'inventory': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price_difference': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'})
        },
        'kishore.physicalrelease': {
            'Meta': {'object_name': 'PhysicalRelease', 'db_table': "'kishore_physicalreleases'", '_ormbases': ['kishore.Product']},
            u'product_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['kishore.Product']", 'unique': 'True', 'primary_key': 'True'}),
            'release': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['kishore.Release']"}),
            'release_format': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'kishore.product': {
            'Meta': {'object_name': 'Product', 'db_table': "'kishore_products'"},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['kishore.Image']", 'symmetrical': 'False'}),
            'inventory': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'})
        },
        'kishore.release': {
            'Meta': {'object_name': 'Release', 'db_table': "'kishore_releases'"},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['kishore.Artist']"}),
            'artwork': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['kishore.Image']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 3, 20, 0, 0)'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'downloadable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'songs': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['kishore.Song']", 'null': 'True', 'blank': 'True'}),
            'soundcloud_url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'streamable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'kishore.song': {
            'Meta': {'object_name': 'Song', 'db_table': "'kishore_songs'"},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['kishore.Artist']"}),
            'artwork': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['kishore.Image']", 'null': 'True', 'blank': 'True'}),
            'audio_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 3, 20, 0, 0)'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'downloadable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'soundcloud_url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'streamable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'track_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['kishore']