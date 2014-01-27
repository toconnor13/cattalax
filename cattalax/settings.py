# Django settings for cattalax project.
import os, sys
db_pw = os.environ['CAT_PW']
amw_email_pw = os.environ['AMW_EMAIL_PWD']
DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

if os.environ['MACHINE_ID']=='cattalax_0':
#	db_host='10.24.18.6'
#	user='bismere0'
	root_dir='/root'
else:
#	db_host = 'localhost'
#	user = 'root'
	root_dir = '/home/sheefrex'

db_host='10.24.18.1'
user='root'

ADMINS = (
     ('Tony O\'Connor', 'toconnor13@gmail.com'),
)

AUTHENTICATION_BACKENDS = (
		'emailusernames.backends.EmailAuthBackend',
		'django.contrib.auth.backends.ModelBackend')

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'cat_dashboard',                      # Or path to database file if using sqlite3.
        'USER': user,                      # Not used with sqlite3.
        'PASSWORD': db_pw,                  # Not used with sqlite3.
        'HOST': db_host,                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

BOWER_COMPONENTS_ROOT = os.path.join(root_dir + '/.virtualenvs/cattalax/cattalax', 'dashboard/static')
# BOWER_PATH = 'usr/bin/bower'
# BOWER_PATH = '~/.virtualenvs/cattalax/bin/bower'
BOWER_INSTALLED_APPS = (
	'jquery#1.9',
	'bootstrap',
	'underscore',
	'd3',
	'nvd3',
	'bootstrap3-datepicker',
	'smalot-bootstrap-datetimepicker',
)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

SITE_URL = os.environ['ALLAMEW_SITE_ID']

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '' 

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
#	'~/.virtualenvs/cattalax/cattalax/components/',	
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
	'djangobower.finders.BowerFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '&amp;z9$&amp;75c$yn#_!3vpx(k^4(qehz6g-5f4mw&amp;0svo2bvtlrc2%l'

TEMPLATE_CONTEXT_PROCESSORS = (

	"django.contrib.auth.context_processors.auth",
	"django.core.context_processors.debug",
	"django.core.context_processors.i18n",
	"django.core.context_processors.media",
	"django.core.context_processors.static",
	"django.core.context_processors.tz",
	"django.core.context_processors.request", # This is added to the default settings
	"django.contrib.messages.context_processors.messages",
	)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'cattalax.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'cattalax.wsgi.application'

cwd=os.getcwd()
template_directory = cwd + '/templates'

TEMPLATE_DIRS = (
		template_directory
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
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
	'dashboard',
	'emailusernames',
	'registration',
	'django_nvd3',
	'djangobower',
	'bootstrapform',
	'debug_toolbar',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

INTERNAL_IPS=('127.0.0.1',)

ACCOUNT_ACTIVATION_DAYS = 7

LOGIN_REDIRECT_URL = ('/dashboard/')
LOGIN_URL = ('/login/')

SERVER_EMAIL = 'allamew.analytics@gmail.com'
EMAIL_USE_TLS=True
EMAIL_HOST='smtp.gmail.com'
EMAIL_HOST_USER='allamew.analytics@gmail.com'
EMAIL_HOST_PASSWORD = amw_email_pw
EMAIL_PORT=587

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
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
