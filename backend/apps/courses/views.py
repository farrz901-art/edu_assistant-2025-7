# 修正视图逻辑
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Course, CourseResource
from .serializers import CourseDesignSerializer, CourseSerializer, CourseEnrollmentSerializer, CourseResourceSerializer
from ai_integration.spark_service import AIService
from shared.exceptions import AIRequestError
from django_filters.rest_framework import DjangoFilterBackend

# {{ edit_1 }}
# class IsTeacher(permissions.BasePermission): # 移除 IsTeacher 权限类
#     def has_permission(self, request, view):
#         return request.user.role == 'teacher'


class CourseListView(generics.ListCreateAPIView):
    """
    获取所有课程或创建新课程。
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['name', 'teacher'] # 导致问题的元凶，暂时注释掉

    def get_queryset(self):
        # {{ edit_3 }}
        # 由于没有用户概念，返回所有课程或根据需要调整
        # 教师只能看到自己创建的课程
        # if self.request.user.role == 'teacher':
        #     return Course.objects.filter(created_by=self.request.user)
        # # 学生只能看到自己参加的课程
        # elif self.request.user.role == 'student':
        #     return self.request.user.enrolled_courses.all()
        return Course.objects.all() # 返回所有课程


    def perform_create(self, serializer):
        # {{ edit_4 }}
        # 由于没有用户概念，不再设置 created_by
        # serializer.save(created_by=self.request.user)
        serializer.save() # 不再保存 created_by


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    获取、更新或删除单个课程。
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    # {{ edit_5 }}
    # permission_classes = [permissions.IsAuthenticated] # 更改为 AllowAny
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # {{ edit_6 }}
        # 权限过滤 - 由于没有用户概念，返回所有对象
        # if self.request.user.role == 'teacher':
        #     return Course.objects.filter(created_by=self.request.user)
        # elif self.request.user.role == 'student':
        #     return self.request.user.enrolled_courses.all()
        return Course.objects.all() # 返回所有课程


class CourseDesignAPIView(APIView):
    # {{ edit_7 }}
    # permission_classes = [permissions.IsAuthenticated, IsTeacher] # 更改为 AllowAny，移除 IsTeacher
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = CourseDesignSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # {{ edit_8 }}
        # 由于没有用户概念，user_id 可以设置为 None 或一个默认值
        ai_service = AIService(user_id=None) # user_id 不再从 request.user 获取
        try:
            content = ai_service.generate_course_content(
                subject=serializer.validated_data['subject'],
                syllabus=serializer.validated_data['syllabus'],
                total_hours=serializer.validated_data.get('total_hours', 40)
            )

            # 返回生成的课程内容，但不立即保存
            return Response({
                'title': serializer.validated_data['title'],
                'subject': serializer.validated_data['subject'],
                'content': content
            })
        except AIRequestError as e:
            return Response({'error': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class CourseEnrollmentAPIView(APIView):
    # {{ edit_9 }}
    # permission_classes = [permissions.IsAuthenticated] # 更改为 AllowAny
    permission_classes = [permissions.AllowAny]

    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        serializer = CourseEnrollmentSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # {{ edit_10 }}
        # 由于没有用户概念，此功能无法正常工作，可以选择禁用或修改逻辑
        # action = serializer.validated_data['action']
        # if action == 'enroll':
        #     course.enrolled_students.add(request.user)
        # elif action == 'withdraw':
        #     course.enrolled_students.remove(request.user)
        #
        # return Response({'status': f'Successfully {action}ed course'})
        return Response({'status': 'Enrollment/Withdrawal functionality is disabled without user authentication.'}, status=status.HTTP_400_BAD_REQUEST)


class CourseResourceViewSet(viewsets.ModelViewSet):
    queryset = CourseResource.objects.all()
    serializer_class = CourseResourceSerializer
    # {{ edit_11 }}
    # permission_classes = [permissions.IsAuthenticated] # 更改为 AllowAny
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        course_id = self.request.query_params.get('course_id')
        if course_id:
            return CourseResource.objects.filter(course_id=course_id)
        return CourseResource.objects.all() # 默认返回所有资源


    def perform_create(self, serializer):
        # {{ edit_12 }}
        # 由于没有用户概念，不再设置 created_by
        # serializer.save(created_by=self.request.user)
        serializer.save() # 不再保存 created_by


class CourseViewSet(viewsets.ModelViewSet):
    """
    一个用于查看和编辑课程实例的视图集。
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]
    
    def list(self, request, *args, **kwargs):
        """
        覆盖list方法以确保正确的数据格式
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': len(serializer.data),
            'next': None,
            'previous': None,
            'results': serializer.data
        })