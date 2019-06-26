## s3:  not for dynamic media and not for whitenoise staticfiles 

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN

class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN  ## can be another bucket 
