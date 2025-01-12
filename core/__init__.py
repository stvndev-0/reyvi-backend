from __future__ import absolute_import, unicode_literals

# Importa Celery como parte del paquete de core
from .celery import app as celery_app

__all__ = ('celery_app',)
