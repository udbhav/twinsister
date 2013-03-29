# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Image'
        db.create_table('kishore_images', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('credit', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('kishore', ['Image'])

        # Adding model 'Artist'
        db.create_table('kishore_artists', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('kishore', ['Artist'])

        # Adding model 'Song'
        db.create_table('kishore_songs', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('artist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kishore.Artist'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 3, 19, 0, 0))),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('soundcloud_url', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('streamable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('downloadable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('audio_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('track_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('kishore', ['Song'])

        # Adding M2M table for field artwork on 'Song'
        db.create_table('kishore_songs_artwork', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('song', models.ForeignKey(orm['kishore.song'], null=False)),
            ('image', models.ForeignKey(orm['kishore.image'], null=False))
        ))
        db.create_unique('kishore_songs_artwork', ['song_id', 'image_id'])

        # Adding model 'Release'
        db.create_table('kishore_releases', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('artist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kishore.Artist'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 3, 19, 0, 0))),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('soundcloud_url', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('streamable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('downloadable', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('kishore', ['Release'])

        # Adding M2M table for field artwork on 'Release'
        db.create_table('kishore_releases_artwork', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('release', models.ForeignKey(orm['kishore.release'], null=False)),
            ('image', models.ForeignKey(orm['kishore.image'], null=False))
        ))
        db.create_unique('kishore_releases_artwork', ['release_id', 'image_id'])

        # Adding M2M table for field songs on 'Release'
        db.create_table('kishore_releases_songs', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('release', models.ForeignKey(orm['kishore.release'], null=False)),
            ('song', models.ForeignKey(orm['kishore.song'], null=False))
        ))
        db.create_unique('kishore_releases_songs', ['release_id', 'song_id'])

        # Adding model 'Product'
        db.create_table('kishore_products', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('inventory', self.gf('django.db.models.fields.IntegerField')(default=-1)),
        ))
        db.send_create_signal('kishore', ['Product'])

        # Adding M2M table for field images on 'Product'
        db.create_table('kishore_products_images', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['kishore.product'], null=False)),
            ('image', models.ForeignKey(orm['kishore.image'], null=False))
        ))
        db.create_unique('kishore_products_images', ['product_id', 'image_id'])

        # Adding model 'DigitalSong'
        db.create_table('kishore_digitalsongs', (
            (u'product_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['kishore.Product'], unique=True, primary_key=True)),
            ('song', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['kishore.Song'], unique=True)),
        ))
        db.send_create_signal('kishore', ['DigitalSong'])

        # Adding model 'DigitalRelease'
        db.create_table('kishore_digitalreleases', (
            (u'product_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['kishore.Product'], unique=True, primary_key=True)),
            ('release', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kishore.Release'])),
            ('audio_format', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('zipfile', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('kishore', ['DigitalRelease'])

        # Adding model 'PhysicalRelease'
        db.create_table('kishore_physicalreleases', (
            (u'product_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['kishore.Product'], unique=True, primary_key=True)),
            ('release', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kishore.Release'])),
            ('release_format', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('kishore', ['PhysicalRelease'])

        # Adding model 'MerchVariant'
        db.create_table('kishore_merchvariants', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('price_difference', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('inventory', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('kishore', ['MerchVariant'])

        # Adding M2M table for field images on 'MerchVariant'
        db.create_table('kishore_merchvariants_images', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('merchvariant', models.ForeignKey(orm['kishore.merchvariant'], null=False)),
            ('image', models.ForeignKey(orm['kishore.image'], null=False))
        ))
        db.create_unique('kishore_merchvariants_images', ['merchvariant_id', 'image_id'])

        # Adding model 'Merch'
        db.create_table('kishore_merch', (
            (u'product_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['kishore.Product'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('kishore', ['Merch'])

        # Adding M2M table for field variants on 'Merch'
        db.create_table('kishore_merch_variants', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('merch', models.ForeignKey(orm['kishore.merch'], null=False)),
            ('merchvariant', models.ForeignKey(orm['kishore.merchvariant'], null=False))
        ))
        db.create_unique('kishore_merch_variants', ['merch_id', 'merchvariant_id'])


    def backwards(self, orm):
        # Deleting model 'Image'
        db.delete_table('kishore_images')

        # Deleting model 'Artist'
        db.delete_table('kishore_artists')

        # Deleting model 'Song'
        db.delete_table('kishore_songs')

        # Removing M2M table for field artwork on 'Song'
        db.delete_table('kishore_songs_artwork')

        # Deleting model 'Release'
        db.delete_table('kishore_releases')

        # Removing M2M table for field artwork on 'Release'
        db.delete_table('kishore_releases_artwork')

        # Removing M2M table for field songs on 'Release'
        db.delete_table('kishore_releases_songs')

        # Deleting model 'Product'
        db.delete_table('kishore_products')

        # Removing M2M table for field images on 'Product'
        db.delete_table('kishore_products_images')

        # Deleting model 'DigitalSong'
        db.delete_table('kishore_digitalsongs')

        # Deleting model 'DigitalRelease'
        db.delete_table('kishore_digitalreleases')

        # Deleting model 'PhysicalRelease'
        db.delete_table('kishore_physicalreleases')

        # Deleting model 'MerchVariant'
        db.delete_table('kishore_merchvariants')

        # Removing M2M table for field images on 'MerchVariant'
        db.delete_table('kishore_merchvariants_images')

        # Deleting model 'Merch'
        db.delete_table('kishore_merch')

        # Removing M2M table for field variants on 'Merch'
        db.delete_table('kishore_merch_variants')


    models = {
        'kishore.artist': {
            'Meta': {'object_name': 'Artist', 'db_table': "'kishore_artists'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
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
            'credit': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
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
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 3, 19, 0, 0)'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'downloadable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'songs': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['kishore.Song']", 'symmetrical': 'False'}),
            'soundcloud_url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'streamable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'kishore.song': {
            'Meta': {'object_name': 'Song', 'db_table': "'kishore_songs'"},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['kishore.Artist']"}),
            'artwork': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['kishore.Image']", 'null': 'True', 'blank': 'True'}),
            'audio_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 3, 19, 0, 0)'}),
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