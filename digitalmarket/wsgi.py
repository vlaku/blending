"""
exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import time
import traceback
import signal
import sys
from django.core.wsgi import get_wsgi_application


from django.conf import settings

## this option removed by whitenoise people at Whitenoise v4 (http://whitenoise.evans.io/en/stable/changelog.html#v4-0)
# from whitenoise.django import DjangoWhiteNoise
# # # Whitenoise is better software than dj-static or static. 

# # from dj_static import Cling, MediaCling
# # application = Cling(get_wsgi_application())
# # application = Cling(MediaCling(get_wsgi_application()))
# # # dj-static + WSGI server like Gunicorn is ok. 
# # # https://github.com/heroku-python/dj-static


## this is wrong for apache+mod_wsgi (setdefault breaks things)
## os.environ.setdefault("DJANGO_SETTINGS_MODULE", "digitalmarket.settings")
os.environ['DJANGO_SETTINGS_MODULE'] = 'digitalmarket.settings'

application = get_wsgi_application()


## this option removed by whitenoise people at Whitenoise v4 (http://whitenoise.evans.io/en/stable/changelog.html#v4-0)
# if not settings.DEBUG:
# 	## for Whitenoise static: 
# 	application = DjangoWhiteNoise(application)



# callable = application 

try:
    application = get_wsgi_application()
except Exception:
    # Error loading applications
    if 'mod_wsgi' in sys.modules:
        traceback.print_exc()
        os.kill(os.getpid(), signal.SIGINT)
        time.sleep(2.5)



## more on uWSGI+nginx: https://coderwall.com/p/ooerda/python-django-apache-ubuntu 
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
