from django.urls import path
from . import views

urlpatterns = [
    # path('users/', views.AdminUserViewSet.as_view({'get': 'list'}), name='admin-users'),
    # path('users/<int:pk>/deactivate/', views.AdminUserViewSet.as_view({'post': 'deactivate'}), name='user-deactivate'),
    # path('users/<int:pk>/activate/', views.AdminUserViewSet.as_view({'post': 'activate'}), name='user-activate'),
    # path('stats/', views.AdminUserViewSet.as_view({'get': 'stats'}), name='admin-stats'),
    # path('activity-logs/', views.AdminUserViewSet.as_view({'get': 'activity_logs'}), name='activity-logs'),
    path('system/', views.SystemMonitorAPIView.as_view(), name='system-monitor'),
]