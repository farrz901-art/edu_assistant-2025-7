# config/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('edu_assistant')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# 配置AI任务队列
app.conf.task_routes = {
    'ai_integration.tasks.*': {'queue': 'ai_queue'},
    'analytics.tasks.*': {'queue': 'analytics_queue'}
}

app.conf.task_acks_late = True
app.conf.worker_prefetch_multiplier = 1
