import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Owad', 'llechowicz@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'company',                      # Or path to database file if using sqlite3.
        'USER': 'company',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'Europe/Warsaw'
LANGUAGE_CODE = 'pl-PL'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
BASE_URL = 'http://test.lule.pl'
 
MEDIA_ROOT = '%s/static_media/' % BASE_PATH
MEDIA_URL = '%s/static_media/' % BASE_URL
STATIC_ROOT = ''
STATIC_URL = '/static_media/'
ADMIN_MEDIA_PREFIX = '%s/admin/' % MEDIA_URL

STATICFILES_DIRS = (
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = 'yfbzri)^(ntvirg(n_xsbnwcbw_9g#wu5=ri_nhha0e9*3ndfa'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'www.urls'

TEMPLATE_DIRS = (
    '/home/owad/workspace/service/www/templates',
    '/home/owad/workspace/django/company/www/templates',
    '/home/owad/workspace/lule.pl/django/company/www/templates'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'www.service',
    'www.account',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

LOGIN_URL = '/zaloguj/'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)
