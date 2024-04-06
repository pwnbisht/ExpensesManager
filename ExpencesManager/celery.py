from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import logging
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ExpencesManager.settings')

app = Celery('ExpancesManager')
app.conf.enable_utc = False

app.conf.update(timezone='Asia/Kolkata')

app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.beat_schedule = {
    'export-data-to-s3-weekly': {
        'task': 'expenses.management.commands.export_data_to_s3',
        'schedule': crontab(day_of_week='monday'),
    },
}


# Configure Celery logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set the desired log level

# Create a FileHandler for Celery logs
file_handler = logging.FileHandler('./celery.log')  # Adjust the file path as needed
file_handler.setLevel(logging.DEBUG)  # Set the desired log level for Celery logs
logger.addHandler(file_handler)

app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@app.task(bind=True, ignore_result=True)
def my_task(self):
    print('Task executed successfully')
