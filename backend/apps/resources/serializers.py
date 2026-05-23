from rest_framework import serializers
from .models import CourseResource, ResourceCollection
from apps.courses.models import Course
import os


class CourseResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseResource
        fields = '__all__'
        read_only_fields = ['created_by', 'version']


class ResourceCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceCollection
        fields = '__all__'
        read_only_fields = ['created_by']


# 添加完整字段验证
class ResourceUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    title = serializers.CharField(max_length=200)
    resource_type = serializers.ChoiceField(choices=CourseResource.RESOURCE_TYPES)
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    description = serializers.CharField(required=False, allow_blank=True)

    def validate_file(self, value):
        max_size = 10 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError("文件大小不能超过10MB")

        # 验证文件类型
        valid_extensions = ['.pdf', '.doc', '.docx', '.ppt', '.pptx', '.zip']
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in valid_extensions:
            raise serializers.ValidationError("不支持的文件类型")
        return value