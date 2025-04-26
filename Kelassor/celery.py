# Kelassor/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Kelassor.settings')




app = Celery('Kelassor')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

