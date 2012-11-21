# Django settings for employment_program project.
#import os

#PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
from django.core.urlresolvers import reverse_lazy
from os.path import join, realpath, dirname, abspath
import sys

# IMPORTANT
# If you have custom site profile check that it inherits
# from pybb.models.PybbProfile or contains all fields from this class.
# AUTH_PROFILE_MODULE = 'pybb.Profile'
AUTH_PROFILE_MODULE = 'common.Person'

#Change to true before deploying into production
ENABLE_SSL = False

SITE_ROOT = join(abspath(dirname(__file__)),"../employment_app")
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
# ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

#DATABASES = {
 #   'default': {
 #       'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
 #       'NAME': os.path.join(PROJECT_ROOT,'employment.db'), # Or path to database file if using sqlite3.
 #   }
#}

import dj_database_url
DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

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
MEDIA_ROOT = join(SITE_ROOT, 'media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
#STATIC_ROOT = '/home/caleb/projects/employment_app/employement app/static'

STATIC_ROOT = join(SITE_ROOT, 'static/')
STATIC_URL = '/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
#STATIC_URL = 'http://localhost:8000/static/'

# Additional locations of static files
STATICFILES_DIRS = (
# Put strings here, like "/home/html/static" or "C:/www/django/static".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
#"/home/caleb/projects/employment_app/employement app/static/"
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    )

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'a1$84#0jj5^8^r0%0k93zgdix#5v0us*z*(ms6#t$oj1lg1!^v'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
    )

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'pybb.context_processors.processor',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pybb.middleware.PybbMiddleware',
    )

ROOT_URLCONF = 'employment_program.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'employment_program.wsgi.application'

TEMPLATE_DIRS = (
# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
    "/home/caleb/projects/employment_app/employment_app/templates/",
    "/home/caleb/projects/employment_app/projects/templates/",    
    "/home/caleb/projects/employment_app/jobsboard/templates/",
#os.path.join(PROJECT_ROOT, "templates"),

)

DEFAULT_FROM_EMAIL = 'webmaster@example.com'

ACCOUNT_ACTIVATION_DAYS = 30

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.formtools',    
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    # django registration
    'registration',
    # django-profiles
    'profiles',
    # django cities light
    'cities_light',
    'south',
    # django pybbm
    'pybb',
    'pytils',
    'sorl.thumbnail',
    'pure_pagination',
    # django faq
    'faq',
    # django-jobsboard
    'tagging',    
    'jobsboard',
    # apps
    'employment_app',    
    'common',
    # django tinymce
    'tinymce',    
    )

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = reverse_lazy('registration_register')

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'emp.app2012@gmail.com'
EMAIL_HOST_PASSWORD = 'empapp2012'


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

# extra fixtures to load when running syncdb
FIXTURE_DIRS = (
    join(SITE_ROOT, '../cities_light_eeuu_fixtures/'),
)

# django-tinymce configuration
TINYMCE_DEFAULT_CONFIG = {
    'custom_undo_redo_levels': 10,

    # General options
    # 'mode': "textareas",
    'theme': "advanced",
    'plugins': "autolink,lists,spellchecker,pagebreak,style,layer,table,save,\
advhr,advimage,advlink,emotions,iespell,inlinepopups,insertdatetime,preview,\
media,searchreplace,print,contextmenu,paste,directionality,fullscreen,\
noneditable,visualchars,nonbreaking,xhtmlxtras,template",

    # Theme options
    'theme_advanced_buttons1': "save,newdocument,|,bold,italic,underline,\
strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,\
styleselect,formatselect,fontselect,fontsizeselect",
    'theme_advanced_buttons2': "cut,copy,paste,pastetext,pasteword,|,search,\
replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,\
unlink,anchor,image,cleanup,help,code,|,insertdate,inserttime,preview,|,\
forecolor,backcolor",
    'theme_advanced_buttons3': "tablecontrols,|,hr,removeformat,visualaid,|,\
sub,sup,|,charmap,emotions,iespell,media,advhr,|,print,|,ltr,rtl,|,fullscreen",
    'theme_advanced_buttons4': "insertlayer,moveforward,movebackward,absolute,\
|,styleprops,spellchecker,|,cite,abbr,acronym,del,ins,attribs,|,visualchars,\
nonbreaking,template,blockquote,pagebreak,|,insertfile,insertimage",
    'theme_advanced_toolbar_location': "top",
    'theme_advanced_toolbar_align': "left",
    'theme_advanced_statusbar_location': "bottom",
    'theme_advanced_resizing': True,

    # Skin options
    'skin': "o2k7",
    'skin_variant': "silver",

    # language
    'language': 'es',
}
TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = True

#--------------------------------
# local settings import
#from http://djangosnippets.org/snippets/1873/
#--------------------------------
try:
    import local_settings
except ImportError:
    print """ 
    -------------------------------------------------------------------------
    You need to create a local_settings.py file.
    -------------------------------------------------------------------------
    """
    import sys 
    sys.exit(1)
else:
    # Import any symbols that begin with A-Z. Append to lists any symbols that
    # begin with "EXTRA_".
    import re
    for attr in dir(local_settings):
        match = re.search('^EXTRA_(\w+)', attr)
        if match:
            name = match.group(1)
            value = getattr(local_settings, attr)
            try:
                globals()[name] += value
            except KeyError:
                globals()[name] = value
        elif re.search('^[A-Z]', attr):
            globals()[attr] = getattr(local_settings, attr)
