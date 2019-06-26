command='~/.virtualenvs/py37/bin/gunicorn'
pythonpath='/media/hd0/data/CODING/python_/django/ecom_nowe/ecom.org'
#bind = '127.0.0.1:8000'
bind='/media/hd0/data/CODING/python_/django/ecom_nowe/ecom.org/run/guni.sock'
workers = 3
user='zyrafka'
errorlog=pythonpath+'/log/gunicorn_error.log'
