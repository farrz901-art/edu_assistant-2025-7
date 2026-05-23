# resources/views.py
import os
import zipfile
from io import BytesIO
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import FileResponse, HttpResponse
from apps.resources.models import CourseResource, ResourceCollection
from .serializers import (
    CourseResourceSerializer,
    ResourceCollectionSerializer,
    ResourceUploadSerializer
)
# {{ edit_1 }}
# from .permissions import IsResourceOwnerOrAdmin, CanAccessResource # 移除自定义权限导入
from shared.exceptions import FileProcessingError

class CourseResourceViewSet(viewsets.ModelViewSet):
    queryset = CourseResource.objects.all()
    serializer_class = CourseResourceSerializer
    parser_classes = (MultiPartParser, FormParser)
    # {{ edit_2 }}
    # permission_classes = [permissions.IsAuthenticated, CanAccessResource] # 更改为 AllowAny
    permission_classes = [permissions.AllowAny]

    # 优化查询性能
    def get_queryset(self):
        # {{ edit_3 }}
        # 由于没有用户概念，不再根据用户过滤
        # queryset = super().get_queryset().select_related(
        #     'course', 'created_by' # created_by 字段已移除
        # ).prefetch_related('course__teachers')
        queryset = super().get_queryset().select_related(
            'course'
        ).prefetch_related('course__teachers') # 移除 created_by，保持其他优化

        # 添加搜索过滤
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset

    def perform_create(self, serializer):
        # {{ edit_4 }}
        # 由于没有用户概念，不再设置 created_by
        # serializer.save(created_by=self.request.user)
        serializer.save() # 不再保存 created_by

    # 添加批量删除
    @action(detail=False, methods=['delete'])
    def bulk_delete(self, request):
        ids = request.data.get('ids', [])
        if not ids:
            return Response({'error': '未选择资源'}, status=status.HTTP_400_BAD_REQUEST)

        resources = self.get_queryset().filter(id__in=ids)
        count = resources.count()
        resources.delete()
        return Response({'status': f'成功删除{count}个资源'})

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """下载资源文件"""
        resource = self.get_object()
        file_path = resource.file.path

        if not os.path.exists(file_path):
            return Response(
                {'error': '文件不存在'},
                status=status.HTTP_404_NOT_FOUND
            )

        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response

    @action(detail=True, methods=['post'])
    def new_version(self, request, pk=None):
        """上传资源新版本"""
        resource = self.get_object()
        serializer = ResourceUploadSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        new_file = serializer.validated_data['file']
        # {{ edit_5 }}
        # new_resource = resource.create_new_version(new_file, request.user) # 移除 request.user
        new_resource = resource.create_new_version(new_file) # 不再传递 user
        return Response(
            CourseResourceSerializer(new_resource).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['get'])
    def by_course(self, request):
        """按课程获取资源"""
        course_id = request.query_params.get('course_id')
        if not course_id:
            return Response(
                {'error': '缺少课程ID参数'},
                status=status.HTTP_400_BAD_REQUEST
            )

        resources = CourseResource.objects.filter(course_id=course_id)
        serializer = self.get_serializer(resources, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def export(self, request):
        """导出多个资源为ZIP包"""
        resource_ids = request.data.get('ids', [])
        resources = CourseResource.objects.filter(id__in=resource_ids)

        if not resources.exists():
            return Response(
                {'error': '未选择任何资源'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 创建内存中的ZIP文件
        zip_buffer = BytesIO()
        try:
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for resource in resources:
                    file_path = resource.file.path
                    if os.path.exists(file_path):
                        # 在ZIP中使用相对路径
                        arcname = f"{resource.course.subject}/{resource.title}_v{resource.version}{os.path.splitext(file_path)[1]}"
                        zipf.write(file_path, arcname=arcname)
        except Exception as e:
            raise FileProcessingError(f"创建ZIP文件失败: {str(e)}")

        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="resources.zip"'
        return response


class ResourceCollectionViewSet(viewsets.ModelViewSet):

    queryset = ResourceCollection.objects.all()
    serializer_class = ResourceCollectionSerializer
    # {{ edit_6 }}
    # permission_classes = [permissions.IsAuthenticated] # 更改为 AllowAny
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        # {{ edit_7 }}
        # 由于没有用户概念，不再设置 created_by
        # serializer.save(created_by=self.request.user)
        serializer.save() # 不再保存 created_by

    @action(detail=True, methods=['post'])
    def add_resources(self, request, pk=None):
        """向集合中添加资源"""
        collection = self.get_object()
        resource_ids = request.data.get('resource_ids', [])

        resources = CourseResource.objects.filter(id__in=resource_ids)
        collection.resources.add(*resources)

        return Response(
            ResourceCollectionSerializer(collection).data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['get'])
    def export(self, request, pk=None):
        """导出整个资源集合"""
        collection = self.get_object()
        resources = collection.resources.all()

        if not resources.exists():
            return Response(
                {'error': '资源集合为空'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 创建内存中的ZIP文件
        zip_buffer = BytesIO()
        try:
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for resource in resources:
                    file_path = resource.file.path
                    if os.path.exists(file_path):
                        arcname = f"{collection.name}/{resource.title}_v{resource.version}{os.path.splitext(file_path)[1]}"
                        zipf.write(file_path, arcname=arcname)
        except Exception as e:
            raise FileProcessingError(f"创建ZIP文件失败: {str(e)}")

        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{collection.name}.zip"'
        return response