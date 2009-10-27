# Django settings for twinsister project.
import os

DEBUG = False
TEMPLATE_DEBUG = False

ADMINS = (
    ('Udbhav Gupta', 'gupta.udbhav@gmail.com'),
    )

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = 'twinsister_django'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# This dynamically discovers the path to the project
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '%sadmin/' % MEDIA_URL

# Make this unique, and don't share it with anybody.
SECRET_KEY = '$^$_xfbwyl7lma@f!w5x&90ryo890qrqcowsk*c&rg!wtdq#db'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    #     'django.template.loaders.eggs.load_template_source',
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    )

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (os.path.join(PROJECT_PATH, 'templates'),)
for root, dirs, files in os.walk(PROJECT_PATH):
    if 'templates' in dirs: TEMPLATE_DIRS = TEMPLATE_DIRS + (os.path.join(root, 'templates'),)

# Context Processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    )

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.comments',
    'django.contrib.databrowse',

    # Requirements
    'sorl.thumbnail',
    'haystack',
    'django_extensions',
    'filebrowser',

    'apps.people',
    'apps.events',
    'apps.music',
    'apps.images',
    'apps.mailing_list',
    'apps.twitter_notify',

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

try:
    from local_settings import *
except ImportError:
    pass
