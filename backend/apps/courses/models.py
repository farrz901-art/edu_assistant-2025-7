# 添加多对多关系和文件大小字段
from django.db import models
# {{ edit_1 }}
# from apps.users.models import User # 移除 User 模型的导入


class Course(models.Model):
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    syllabus = models.TextField()
    content = models.TextField()
    # {{ edit_2 }}
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_courses') # 移除创建者字段
    # enrolled_students = models.ManyToManyField(User, related_name='enrolled_courses', blank=True) # 移除学生注册字段
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CourseResource(models.Model):
    RESOURCE_TYPES = (
        ('slide', '课件'),
        ('exercise', '练习'),
        ('reference', '参考资料'),
        ('other', '其他'),
    )

    course = models.ForeignKey(Course, related_name='course_resources_from_courses_app', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    file = models.FileField(upload_to='course_resources/')
    file_size = models.BigIntegerField(default=0)  # 新增文件大小字段
    version = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True, null=True)
    # {{ edit_3 }}
    # created_by = models.ForeignKey(User, related_name='course_resources_created_in_courses_app', on_delete=models.CASCADE) # 移除创建者字段
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):        # 自动计算文件大小
        if self.file:
            self.file_size = self.file.size
        super().save(*args, **kwargs)
