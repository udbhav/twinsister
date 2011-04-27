# Django settings for twinsister project.
import os

DEBUG = False
TEMPLATE_DEBUG = False

ADMINS = (
    ('Udbhav Gupta', 'gupta.udbhav@gmail.com'),
    )

MANAGERS = (
    ('Udbhav Gupta', 'gupta.udbhav@gmail.com'),
)

MANAGERS = ADMINS

#DATABASE_ENGINE = 'postgresql_psycopg2'
DATABASE_NAME = 'twinsister_django'
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

TIME_ZONE = 'America/New_York'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = False

# This is the location of the src directory of our project
# It's used to determine a whole range of other settings
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

# Media stuff, see http://docs.djangoproject.com/en/dev/ref/settings/ for more information
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')
MEDIA_URL = 'http://twinsisterroot.s3.amazonaws.com/'
ADMIN_MEDIA_PREFIX = '/media/admin/'

SECRET_KEY = '$^$_xfbwyl7lma@f!w5x&90ryo890qrqcowsk*c&rg!wtdq#db'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    #     'django.template.loaders.eggs.load_template_source',
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    PROJECT_PATH + '/templates'
    )

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'context_processors.current_site',
    )

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.databrowse',

    # Dependencies
    'haystack',
    'django_extensions',
    'filebrowser',
    'oembed',
    'debug_toolbar',
    'imagekit',
    #FIXME
    #'south',

    # Apps Yo!
    'apps.data',
    'apps.people',
    'apps.events',
    'apps.music',
    'apps.images',
    'apps.store',
    #'apps.twitter_notify',
    )

HAYSTACK_SITECONF = 'search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = os.path.join(PROJECT_PATH, 'whoosh')

# Twitter credentials for twitter_notify
TWITTER_USERNAME = ''
TWITTER_PASSWORD = ''

# bit.ly credentials for twitter_notify
BITLY_USERNAME = ''
BITLY_API_KEY = ''

# Filebrowser settings
FILEBROWSER_URL_FILEBROWSER_MEDIA = '/media/filebrowser/'
FILEBROWSER_MAX_UPLOAD_SIZE = 104857600 # 100MB
FILEBROWSER_EXTENSIONS = {
    'Folder': [''],
    'Image': ['.jpg','.jpeg','.gif','.png','.tif','.tiff'],
    'Video': ['.mov','.wmv','.mpeg','.mpg','.avi','.rm'],
    'Document': ['.pdf','.doc','.rtf','.txt','.xls','.csv','.zip','.gz','.tar','.rar'],
    'Audio': ['.mp3','.mp4','.wav','.aiff','.midi','.m4p'],
    'Code': ['.html','.py','.js','.css']
}

# Settings for Flickr
FLICKR_API_KEY = ''

# Django Debug Toolbar
INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

# Oembed
OEMBED_MAX_WIDTH = '600'
OEMBED_MAX_HEIGHT = '600'

# Cache Settings
CACHE_BACKEND = ''
CACHE_MIDDLEWARE_SECONDS = 60*10


# Session Settings for splash page
SESSION_COOKIE_AGE = 2592000

# Storage backend for S3
#DEFAULT_FILE_STORAGE = 'backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_STORAGE_BUCKET_NAME = ''

#Store & Paypal
STORE_ADMINS = ['gupta.udbhav@gmail.com',]
PAYPAL_RECEIVER_EMAIL = 'band@twinsistermusic.com'
PAYPAL_NOTIFY_URL = "http://www.example.com/your-ipn-location/"
PAYPAL_RETURN_URL = "http://www.example.com/your-return-location/"
PAYPAL_CANCEL_URL = "http://www.twinsistermusic.com"
PAYPAL_SUBMIT_URL = 'https://www.paypal.com/cgi-bin/webscr'

try:
    from local_settings import *
except ImportError:
    pass
