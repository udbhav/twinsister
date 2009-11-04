import os
import sys
import site

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
os.environ['PYTHON_EGG_CACHE'] = '/home/udbhav/www/django/.python_eggs'

site.addsitedir('/home/udbhav/www/django/twinsister/env/lib/python2.6/site-packages')
sys.path.append('/home/udbhav/www/django/twinsister/src')

import django.core.handlers.wsgi
_application = django.core.handlers.wsgi.WSGIHandler()

def application(environ, start_response):
        environ['wsgi.url_scheme'] = environ.get('HTTP_X_URL_SCHEME', 'http')
        return _application(environ, start_response)
