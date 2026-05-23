# resources/permissions.py
from rest_framework import permissions


class IsResourceOwnerOrAdmin(permissions.BasePermission):
    """检查用户是否是资源创建者或管理员"""

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        return obj.created_by == request.user


# 修正权限逻辑，允许教师访问自己课程的所有资源
class CanAccessResource(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role == 'admin':
            return True
        if user.role == 'teacher' and obj.course.teachers.filter(id=user.id).exists():
            return True
        if user.role == 'student' and obj.course in user.enrolled_courses.all():
            return True
        return False
