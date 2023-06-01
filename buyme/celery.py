import os
from celery import Celery
from decouple import config

# set the default Django settings module for the 'celery' program.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', config('SETTINGS'))
app = Celery('buyme')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
