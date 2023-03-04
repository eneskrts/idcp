from datetime import timedelta

from celery.schedules import crontab


CELERYBEAT_SCHEDULE = {

    'xxx': {
        'task': 'appointment.tasks.get_crawler_data',
        'schedule': timedelta(days=1)
 #       'kwargs': ({

         #})
    }
}