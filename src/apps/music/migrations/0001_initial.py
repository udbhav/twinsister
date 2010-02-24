
from south.db import db
from django.db import models
from apps.music.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Archive'
        db.create_table('music_archive', (
            ('id', orm['music.Archive:id']),
            ('release', orm['music.Archive:release']),
            ('archive', orm['music.Archive:archive']),
            ('file_type', orm['music.Archive:file_type']),
        ))
        db.send_create_signal('music', ['Archive'])
        
        # Adding model 'Stem'
        db.create_table('music_stem', (
            ('id', orm['music.Stem:id']),
            ('release', orm['music.Stem:release']),
            ('archive', orm['music.Stem:archive']),
            ('description', orm['music.Stem:description']),
        ))
        db.send_create_signal('music', ['Stem'])
        
        # Adding model 'Credit'
        db.create_table('music_credit', (
            ('id', orm['music.Credit:id']),
            ('song', orm['music.Credit:song']),
            ('name', orm['music.Credit:name']),
            ('instruments', orm['music.Credit:instruments']),
        ))
        db.send_create_signal('music', ['Credit'])
        
        # Adding model 'MusicData'
        db.create_table('music_musicdata', (
            ('data_ptr', orm['music.MusicData:data_ptr']),
            ('artwork', orm['music.MusicData:artwork']),
            ('official', orm['music.MusicData:official']),
        ))
        db.send_create_signal('music', ['MusicData'])
        
        # Adding model 'Song'
        db.create_table('music_song', (
            ('musicdata_ptr', orm['music.Song:musicdata_ptr']),
            ('band', orm['music.Song:band']),
            ('file', orm['music.Song:file']),
            ('track_number', orm['music.Song:track_number']),
            ('older_version', orm['music.Song:older_version']),
            ('newer_version', orm['music.Song:newer_version']),
        ))
        db.send_create_signal('music', ['Song'])
        
        # Adding model 'Release'
        db.create_table('music_release', (
            ('musicdata_ptr', orm['music.Release:musicdata_ptr']),
            ('band', orm['music.Release:band']),
            ('type', orm['music.Release:type']),
            ('buy_link', orm['music.Release:buy_link']),
        ))
        db.send_create_signal('music', ['Release'])
        
        # Adding ManyToManyField 'Song.composers'
        db.create_table('music_song_composers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('song', models.ForeignKey(orm.Song, null=False)),
            ('person', models.ForeignKey(orm['people.Person'], null=False))
        ))
        
        # Adding ManyToManyField 'Release.songs'
        db.create_table('music_release_songs', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('release', models.ForeignKey(orm.Release, null=False)),
            ('song', models.ForeignKey(orm.Song, null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Archive'
        db.delete_table('music_archive')
        
        # Deleting model 'Stem'
        db.delete_table('music_stem')
        
        # Deleting model 'Credit'
        db.delete_table('music_credit')
        
        # Deleting model 'MusicData'
        db.delete_table('music_musicdata')
        
        # Deleting model 'Song'
        db.delete_table('music_song')
        
        # Deleting model 'Release'
        db.delete_table('music_release')
        
        # Dropping ManyToManyField 'Song.composers'
        db.delete_table('music_song_composers')
        
        # Dropping ManyToManyField 'Release.songs'
        db.delete_table('music_release_songs')
        
    
    
    models = {
        'data.data': {
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'header_image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.HeaderImage']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'posted_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Person']"}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 2, 23, 20, 52, 5, 796834)'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'data.headerimage': {
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'images.gallery': {
            'imagebase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['images.ImageBase']", 'unique': 'True', 'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['images.Image']"})
        },
        'images.image': {
            'caption': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'credit': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['people.Person']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'images.imagebase': {
            'data_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['data.Data']", 'unique': 'True', 'primary_key': 'True'})
        },
        'music.archive': {
            'archive': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'file_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'release': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['music.Release']"})
        },
        'music.credit': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instruments': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Person']"}),
            'song': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['music.Song']"})
        },
        'music.musicdata': {
            'artwork': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['images.Gallery']", 'null': 'True', 'blank': 'True'}),
            'data_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['data.Data']", 'unique': 'True', 'primary_key': 'True'}),
            'official': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'music.release': {
            'band': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Band']"}),
            'buy_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'musicdata_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['music.MusicData']", 'unique': 'True', 'primary_key': 'True'}),
            'songs': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['music.Song']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'music.song': {
            'band': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Band']"}),
            'composers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['people.Person']", 'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'musicdata_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['music.MusicData']", 'unique': 'True', 'primary_key': 'True'}),
            'newer_version': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'older'", 'null': 'True', 'to': "orm['music.Song']"}),
            'older_version': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'newer'", 'null': 'True', 'to': "orm['music.Song']"}),
            'track_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'music.stem': {
            'archive': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'release': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['music.Release']"})
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
    
    complete_apps = ['music']
