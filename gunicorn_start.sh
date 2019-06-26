#!/bin/bash
APPNAME='digitalmarket'
# PYTHONPATH='~/Env/virtual_ecom'
SOCKFILE='/media/hd0/data/CODING/python_/django/ecom_nowe/ecom.org/run/guni.sock'
DIR='/media/hd0/data/CODING/python_/django/ecom_nowe/ecom.org/'

LOGFILE='/media/hd0/data/CODING/python_/django/ecom_nowe/ecom.org/logs/gunicorn.log'
LOGDIR=$(dirname $LOGFILE)


USER=zyrafka
GROUP=zyrafka
WORKERS=3

#BIND=unix:$SOCKFILE
BIND=unix:///media/hd0/data/CODING/python_/django/ecom_nowe/ecom.org/run/guni.sock


DJANGO_SETTINGS_MODULE='digitalmarket.settings'
DJANGO_WSGI_MODULE='digitalmarket.wsgi'

#LOG_LEVEL=error
LOG_LEVEL=debug

echo "Starting $APPNAME as $USER"

cd $DIR
#workon py36 ale nie py37
source ~/Env/virtual_ecom/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DIR:$PYTHONPATH


# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR


exec gunicorn ${DJANGO_WSGI_MODULE}:application \
--name $APPNAME \
--workers $WORKERS \
--user=$USER \
--group=$GROUP \
--bind=$BIND \
--log-level=$LOG_LEVEL \
--log-file=-

