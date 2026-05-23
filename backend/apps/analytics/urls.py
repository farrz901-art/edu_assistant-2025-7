# backend/apps/analytics/urls.py
from django.urls import path
from .views import LearningAnalyticsAPIView

urlpatterns = [
    path('', LearningAnalyticsAPIView.as_view(), name='analytics'),
]
