
import os
#from os import environ  # environ.get('xxx','')
from django.conf import settings
from decouple import config
#from decouple import Csv
from unipath import Path
import dj_database_url
# from dj_database_url import parse as db_url
import urllib.parse as urlparse
import psycopg2
from builtins import bool

# import django_heroku
# import boto3
# from storages.backends.s3boto3 import S3Boto3Storage


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = config('SECRET_KEY')
DEBUG=False

ENVIRONMENT_PATH = os.path.abspath(os.path.dirname(__file__))
ENVIRONMENT_NAME = 'Production'
ENVIRONMENT_COLOR = 'red'

ALLOWED_HOSTS=config('ALLOWED_HOSTS')

# sprawdzic co jest w .env
# DATABASE_URL = config('DATABASE_URL')
DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'), conn_max_age=500)
}

# ustawienia sa pod postgres:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DATABASE_NAME',''),
        'USER': config('DATABASE_USER',''),
        'PASSWORD': config('DATABASE_PASSWORD',''),
        'HOST': config('DATABASE_HOST',''),
        'PORT': config('DATABASE_PORT',''),
    }
}


# ustawienia sa pod sqlite --- nie powinno byc nigdy w proukcji:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'mydatabase'),
#     }
# }



# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    # for heroku static; WhiteNoise is not suitable for serving user-uploaded 'media' files.
    'django.contrib.staticfiles',
    # 'mod_wsgi.server',
    ## my proj with __init__.py:
    'accounts',
    'analytics',
    'billing',
    'checkout',
    'dashboard',
    'digitalmarket',
    'products',
    'sellers',
    'tags',
    # third party:
    'anymail',
    # 'switchboard_operator', # trzeba sklonowac
    'bootstrap4',
    'django_extensions',
    'widget_tweaks',
    'stripe',
    # 'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'csp.middleware.CSPMiddleware',  # needs to be configured properly.
]
ANYMAIL = {
    "SENDGRID_API_KEY": config("SENDGRID_API_KEY"),
    # 'WEBHOOK_SECRET': '<a random string>:<another random string>',
    'WEBHOOK_SECRET': 'jWcmeCxb4ox2NyZY:SfZRcMwL8ddrcDc8'
    # if you want webhooks -status etc.  An easy way to generate a random secret is to run this command in a shell:
    # python -c "from django.utils import crypto; print(':'.join(crypto.get_random_string(16) for _ in range(2)))"
}

ROOT_URLCONF = 'digitalmarket.urls'


TEMPLATES = [ {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #'django.core.context_processors.static',
                'accounts.context_processors.from_settings',
            ],
        },
    },
]




WSGI_APPLICATION = 'digitalmarket.wsgi.application'



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


#------------static + media ----------


## niepoprawne wciaganie static files
# STATICFILES_FINDERS = (
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     #'django.contrib.staticfiles.finders.AppDirectoriesFinder',    #causes verbose duplicate notifications in django 1.9
# )


# places where static files can be found
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    )



# whitenoise  (simplified) static file serving.
# --- s3 not compatible with whitenoise static as s3 cannot serve compressed ---
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# static files  -- local server ---
STATIC_URL='/static/'
# media files  -- local server ---
MEDIA_URL='/media/'


# --- other than heroku (can be pythonanywhere)  --local --
# dokad ma 'wciagac':
STATIC_ROOT=os.path.join(os.path.dirname(BASE_DIR), "static_cdn", "staticfiles")
MEDIA_ROOT=os.path.join(os.path.dirname(BASE_DIR), "static_cdn", "media")


# static files  -- remote ---
# -- however s3 not compatible with whitenoise<4 as cannot serve compressed --
# STATIC_HOST=config('STATIC_HOST')
# STATIC_URL=STATIC_HOST+'/static/'
# STATIC_ROOT=config('STATIC_ROOT')



# --- media files -- remote --  (could be for heroku) ---
# --- not s3: does not process/serve dynamic media ---
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# MEDIA_HOST=config('MEDIA_HOST')
# MEDIA_URL=MEDIA_HOST+'/media/'
# # ## media files storage:
# DEFAULT_FILE_STORAGE=MEDIA_URL
# dokad ma 'wciagac':
# MEDIA_ROOT=config('MEDIA_ROOT')


# DELETE_MEDIA_FILE_METHOD = 'core.utils.delete_file_local'

#----------------
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'products:list'
LOGOUT_REDIRECT_URL = 'accounts:farewell'
# LOGIN_REDIRECT_URL = 'sellers:dashboard'

#---------- email -------------

EMAIL_BACKEND = config('EMAIL_BACKEND')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='')
EMAIL_HOST = config('EMAIL_HOST', default='')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
#SENDGRID_API_KEY = config('SENDGRID_API_KEY')
EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=False, cast=bool)
DISALLOWED_USER_AGENTS = config('DISALLOWED_USER_AGENTS')

EMAIL_SUBJECT_PREFIX = '[]' # powinna byc nazwa mojej domeny
PASSWORD_RESET_TIMEOUT_DAYS = 3 # link validity

admin_email=config('admin_email')
ADMINS=(('Admin',admin_email),)
MANAGERS = ADMINS


#----------------------------

# This will store all of the session data in the database on your server, while
# only sending a small ID to the client so that they don’t have all of the data:
# SESSION_ENGINE="django.contrib.sessions.backends.db"





# Your web server must redirect all HTTP traffic to HTTPS, and only transmit HTTPS requests to Django.
# You have your SSL/TLS Security Certificate installed (on one of those services: Heroku, Elastic Beanstalk, Linode, Webfaction, and Digital Ocean)
CORS_ALLOW_CREDENTIALS=True
CORS_ORIGIN_ALLOW_ALL=True
CORS_REPLACE_HTTPS_REFERER=True
CORS_REPLACE_HTTPS_REFERER      = True
CORS_ORIGIN_WHITELIST = (
    'localhost', 'vlaku.pythonanywhere.com',
)
HOST_SCHEME                     = "https://"
# podobno hsts blokuje self-signed cert
SECURE_HSTS_INCLUDE_SUBDOMAINS  = True
SECURE_HSTS_SECONDS             = 63072000

# dont do SECURE_HSTS_PRELOAD=True in localhost https unless you understand the implications
SECURE_HSTS_PRELOAD             = True

# SECURE_HSTS_SECONDS='' # If your entire site is served only over SSL, you may want to consider setting a value and enabling HTTP Strict Transport Security.
SECURE_FRAME_DENY               = True
SECURE_CONTENT_TYPE_NOSNIFF     = True
SECURE_BROWSER_XSS_FILTER       = True
X_FRAME_OPTIONS                 = 'DENY'
# X_FRAME_OPTIONS default is SAMEORIGIN

SECURE_SSL_REDIRECT             = True
## Unless your site should be available over both SSL and non-SSL connections, you may want to either set this setting True or configure a load balancer or reverse-proxy server to redirect all connections to HTTPS.
SESSION_COOKIE_SECURE           = True
CSRF_COOKIE_SECURE              = True
# CSRF_TRUSTED_ORIGINS=['vlaku.icu']
CSRF_TRUSTED_ORIGINS=['127.0.0.1','vlaku.pythonanywhere.com']
# CSRF_COOKIE_DOMAIN='vlaku.icu'
CSRF_COOKIE_DOMAIN='vlaku.pythonanywhere.com'
# https://pypi.org/project/django-cors-headers/
# https://github.com/ottoyiu/django-cors-headers/
# https://github.com/zestedesavoir/django-cors-middleware
# https://www.html5rocks.com/en/tutorials/cors/#toc-cors-from-jquery
