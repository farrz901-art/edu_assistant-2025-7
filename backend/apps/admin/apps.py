# backend/apps/admin/apps.py
from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig

class AdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.admin'
