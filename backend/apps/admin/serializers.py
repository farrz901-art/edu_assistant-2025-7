from rest_framework import serializers
# from apps.users.models import User
from apps.courses.models import Course
from apps.analytics.models import UserActivityLog

# class AdminUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'role', 'is_active', 'date_joined']

class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivityLog
        fields = ['id', 'user', 'action', 'timestamp']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'subject', 'created_at']
