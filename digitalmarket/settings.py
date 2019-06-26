'''
switch for Django production settings for peanuts project.
'''
import os
#from os import environ  # environ.get('xxx','')
from django.conf import settings
from decouple import config
# from decouple import Csv
from unipath import Path
import dj_database_url
# from dj_database_url import parse as db_url
import urllib.parse as urlparse
import psycopg2
from builtins import bool

#import django_heroku
# import boto3
# from storages.backends.s3boto3 import S3Boto3Storage


DEBUG=config('DEBUG', default=False, cast=bool)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS')

ROOT_URLCONF = 'digitalmarket.urls' # tylko jesli wszystkie urls sa w tym tym jednym miejscu albo wskazuje ono jako glowne gdzie jest reszta


## tester
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "emails_file")
FILE_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
WORKING_EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_BACKEND_LIST = [WORKING_EMAIL_BACKEND, FILE_BACKEND]
#####################################################


if DEBUG:
    try:
        from .settings_local import *
    except ImportError:
        print('Looks like a local ImportError')
else:
    try:
         from .settings_pythonanywhere import *
#        from .settings_production_sqlite import *
#        from .settings_production import *
    except ImportError:
        print('production ImportError')

