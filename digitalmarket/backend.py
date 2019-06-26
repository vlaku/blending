# https://github.com/KristianOellegaard/django-multiple-email-backends/tree/master/django_multiple_email_backends
#
#   TO BE TESTED
#
# #-*- coding: utf-8 -*-
import os
from . import settings
from decouple import config
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings
from django.core.mail import get_connection

EMAIL_FILE_PATH = os.path.join(settings.BASE_DIR, "emails_file")
EMAIL_BACKEND = "django_multiple_email_backends.backend.CombinedEmailBackend"
WORKING_EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_BACKEND_LIST = [WORKING_EMAIL_BACKEND,
                      'django.core.mail.backends.filebased.EmailBackend']


class CombinedEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        for backend in getattr(settings, "EMAIL_BACKEND_LIST", []):
            get_connection(backend).send_messages(email_messages)
        return len(email_messages)
