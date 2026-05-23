# # admin/views.py
from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.conf import settings
from apps.analytics.models import UserActivityLog
from apps.courses.models import Course
from .serializers import  UserActivitySerializer, CourseSerializer


# class AdminUserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = AdminUserSerializer
#     permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
#
#     def get_queryset(self):
#         return User.objects.all()
#
#     @action(detail=False, methods=['get'])
#     def stats(self, request):
#         total = User.objects.count()
#         teachers = User.objects.filter(role='teacher').count()
#         students = User.objects.filter(role='student').count()
#         active = User.objects.filter(is_active=True).count()
#
#         last_7_days = timezone.now() - timedelta(days=7)
#         active_recent = User.objects.filter(
#             last_login__gte=last_7_days
#         ).count()
#
#         return Response({
#             'total': total,
#             'teachers': teachers,
#             'students': students,
#             'active': active,
#             'inactive': total - active,
#             'active_recent': active_recent
#         })
#
#     @action(detail=False, methods=['get'])
#     def activity_logs(self, request):
#         logs = UserActivityLog.objects.order_by('-timestamp')[:100]
#         serializer = UserActivitySerializer(logs, many=True)
#         return Response(serializer.data)
#
#     @action(detail=True, methods=['post'])
#     def deactivate(self, request, pk=None):
#         """停用用户"""
#         user = self.get_object()
#         if user == request.user:
#             return Response(
#                 {'error': '不能停用自己'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#         user.is_active = False
#         user.save()
#         return Response({'status': '用户已停用'})
#
#     @action(detail=True, methods=['post'])
#     def activate(self, request, pk=None):
#         """激活用户"""
#         user = self.get_object()
#         user.is_active = True
#         user.save()
#         return Response({'status': '用户已激活'})
#
#     @action(detail=True, methods=['get'])
#     def enrolled_courses(self, request, pk=None):
#         """获取用户参与的课程"""
#         user = self.get_object()
#         if user.role == 'teacher':
#             courses = user.taught_courses.all()
#         elif user.role == 'student':
#             courses = user.enrolled_courses.all()
#         else:
#             courses = Course.objects.none()
#
#         serializer = CourseSerializer(courses, many=True)
#         return Response(serializer.data)


class SystemMonitorAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get(self, request):
        # 数据库状态
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT pg_size_pretty(pg_database_size(current_database()))")
            db_size = cursor.fetchone()[0]

            cursor.execute("SELECT count(*) FROM pg_stat_activity")
            db_connections = cursor.fetchone()[0]

        # 资源使用情况
        total_size = 0
        if hasattr(default_storage, 'size'):
            import os
            total_size = sum(
                os.path.getsize(os.path.join(dirpath, filename))
                for dirpath, _, filenames in os.walk(settings.MEDIA_ROOT)
                for filename in filenames
            ) / (1024 * 1024)  # MB

        # 简化AI使用统计
        ai_usage = {
            'requests_today': 0,
            'requests_total': 0
        }

        return Response({
            'database': {
                'size': db_size,
                'connections': db_connections
            },
            'storage': {
                'total_size_mb': round(total_size, 2),
                'media_root': settings.MEDIA_ROOT
            },
            'ai_usage': ai_usage
        })
