# 添加缺失的序列化器
from rest_framework import serializers
from .models import Course, CourseResource


class CourseDesignSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    subject = serializers.CharField(max_length=100)
    syllabus = serializers.CharField()
    total_hours = serializers.IntegerField(default=40, min_value=10, max_value=100)


class CourseEnrollmentSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['enroll', 'withdraw'])


class CourseResourceSerializer(serializers.ModelSerializer):
    file_size = serializers.SerializerMethodField()

    class Meta:
        model = CourseResource
        fields = '__all__'
        read_only_fields = ['created_by', 'version', 'file_size']

    def get_file_size(self, obj):
        # 自动转换字节为可读格式
        if obj.file_size < 1024:
            return f"{obj.file_size} B"
        elif obj.file_size < 1024 * 1024:
            return f"{obj.file_size / 1024:.1f} KB"
        else:
            return f"{obj.file_size / (1024 * 1024):.1f} MB"


class CourseSerializer(serializers.ModelSerializer):
    resources = CourseResourceSerializer(many=True, read_only=True)
    # Explicitly define all fields for robust serialization
    id = serializers.ReadOnlyField()
    name = serializers.CharField(source='title', read_only=True)
    description = serializers.CharField(source='syllabus', read_only=True)

    class Meta:
        model = Course
        # Define the fields to be exposed to the frontend
        fields = ['id', 'name', 'description', 'resources', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']