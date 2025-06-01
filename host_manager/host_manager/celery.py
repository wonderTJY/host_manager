import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'host_manager.settings')

app = Celery('host_manager')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# 8小时检查轮换以及每天生成统计
app.conf.beat_schedule = {
    'rotate-passwords-every-8-hours': {
        'task': 'app.tasks.rotate_host_passwords',
        'schedule': crontab(minute=0, hour='*/8'),
        #'schedule': crontab(minute='*/1'),
    },
    'generate-daily-statistics': {
        'task': 'app.tasks.generate_host_statistics',
        'schedule': crontab(minute=0, hour=0),
        #'schedule': crontab(minute=6, hour=23),
    },
}
