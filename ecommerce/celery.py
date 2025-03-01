
'''
For using an in-Memory Queue for Asynchronous Processing , I have implemented it using celery with redis
which processes orders asynchronously.
the celery queue will immediately queue the order for processing (non-blocking).
Celery processes each order asynchronously, updating the status.
'''

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")

celery_app = Celery("ecommerce.orders")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")

celery_app.autodiscover_tasks()

@celery_app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")