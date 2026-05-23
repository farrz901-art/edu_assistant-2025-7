from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from shared.decorators import handle_view_exception
from .models import LearningAnalytics
from apps.courses.models import Course
from .models import LearningAnalytics
from .serializers import LearningAnalyticsSerializer
from ..courses.serializers import CourseSerializer


# backend/apps/analytics/views.py
class LearningAnalyticsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @handle_view_exception
    def get(self, request):
        # 学生查看自己的学情
        if request.user.role == 'student':
            analytics = get_object_or_404(
                LearningAnalytics,
                student=request.user
            )
            return Response(LearningAnalyticsSerializer(analytics).data)

        # 教师查看课程学情
        elif request.user.role == 'teacher':
            course_id = request.query_params.get('course_id')
            if not course_id:
                return Response(
                    {'error': '缺少课程ID参数'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 验证教师是否教授该课程
            if not Course.objects.filter(id=course_id, teacher=request.user).exists():
                return Response(
                    {'error': '无权访问该课程数据'},
                    status=status.HTTP_403_FORBIDDEN
                )

            analytics = LearningAnalytics.objects.filter(
                course_id=course_id
            ).select_related('student')

            course = Course.objects.get(id=course_id)
            return Response({
                'course': CourseSerializer(course).data,
                'analytics': LearningAnalyticsSerializer(analytics, many=True).data
            })

        # 管理员查看所有学情
        elif request.user.role == 'admin':
            analytics = LearningAnalytics.objects.all()
            return Response(LearningAnalyticsSerializer(analytics, many=True).data)

        return Response(
            {'error': '无权访问该资源'},
            status=status.HTTP_403_FORBIDDEN
        )