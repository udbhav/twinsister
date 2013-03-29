
from south.db import db
from django.db import models
from apps.mailing_list.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Subscriber'
        db.create_table('mailing_list_subscriber', (
            ('id', orm['mailing_list.Subscriber:id']),
            ('email', orm['mailing_list.Subscriber:email']),
        ))
        db.send_create_signal('mailing_list', ['Subscriber'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Subscriber'
        db.delete_table('mailing_list_subscriber')
        
    
    
    models = {
        'mailing_list.subscriber': {
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }
    
    complete_apps = ['mailing_list']
