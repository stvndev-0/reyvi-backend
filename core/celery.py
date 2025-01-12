from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'eliminar-usuarios-no-verificados': {
        'task': 'authentication.task.account_not_verify',
        'schedule': 600.0,  # Cada 10 minutos
    },
}