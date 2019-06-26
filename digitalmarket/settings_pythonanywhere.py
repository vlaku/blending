import os
from django.conf import settings
from decouple import config
import dj_database_url
#from decouple import Csv
#from unipath import Path
#from dj_database_url import parse as db_url
#import psycopg2
#from builtins import bool


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = config('SECRET_KEY')
DEBUG=False

ALLOWED_HOSTS=config('ALLOWED_HOSTS')


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    #'mod_wsgi.server',
    # my proj with __init__.py:
    'accounts',
    'analytics',
    'billing',
    'checkout',
    'dashboard',
    'products',
    'sellers',
    'tags',
    # third party:
    'anymail',
    # 'inbound_email',
    'bootstrap4',
    'django_extensions',
    'widget_tweaks',
    'stripe',
]

# for 'inbound_email',
INBOUND_EMAIL_PARSER = 'inbound_email.backends.sendgrid.SendGridRequestParser'
INBOUND_EMAIL_LOG_REQUESTS = True
INBOUND_EMAIL_RESPONSE_200 = True
EMAIL_BACKEND = config('EMAIL_BACKEND')
# files email:
# EMAIL_FILE_PATH=os.path.join(BASE_DIR, "emails_file")  ## if 2 backends




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

#
# DATABASES = {
#     'default': dj_database_url.config(
#         default=config('DATABASE_URL')
#     )
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'mydatabase'),
    }
}

# whitenoise:
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

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


ANYMAIL = {
    'SENDGRID_API_KEY': config('SENDGRID_API_KEY'),
    'WEBHOOK_SECRET': config('WEBHOOK_SECRET'),
}



# for admin warning colors in production
ENVIRONMENT_PATH = os.path.abspath(os.path.dirname(__file__))
ENVIRONMENT_NAME = 'Production'
ENVIRONMENT_COLOR = 'red'


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


STATIC_URL = '/static/'  # ideal: http://static.vlaku.icu
MEDIA_URL = '/media/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    )

# for whitenoise:
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
## whitenoise default:
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_ROOT =   os.path.join(os.path.dirname(BASE_DIR), "static_cdn", "media")


LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'products:list'
LOGOUT_REDIRECT_URL = 'accounts:farewell'





#----------------------------

SESSION_ENGINE="django.contrib.sessions.backends.db"

#----------------------------


CORS_REPLACE_HTTPS_REFERER      = True
HOST_SCHEME                     = "https://"
SECURE_PROXY_SSL_HEADER         = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT             = True
SESSION_COOKIE_SECURE           = True
CSRF_COOKIE_SECURE              = True
SECURE_HSTS_INCLUDE_SUBDOMAINS  = True
SECURE_HSTS_SECONDS             = 31536000
SECURE_FRAME_DENY               = True
X_FRAME_OPTIONS                 ='DENY'
# X_FRAME_OPTIONS default is SAMEORIGIN
CSRF_COOKIE_SECURE              =True
SESSION_COOKIE_SECURE           =True
SECURE_CONTENT_TYPE_NOSNIFF     =True
SECURE_BROWSER_XSS_FILTER       =True

PASSWORD_RESET_TIMEOUT_DAYS = 3
