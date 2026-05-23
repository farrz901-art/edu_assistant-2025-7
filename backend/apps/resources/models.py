# data_models/resource.py
import os
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from apps.courses.models import Course
# {{ edit_1 }}
# from apps.users.models import User # 移除 User 模型的导入
from django.urls import reverse
from django.core.files.storage import default_storage
import logging
logger = logging.getLogger(__name__)


def resource_upload_path(instance, filename):
    """生成资源文件存储路径"""
    return f"resources/{instance.course.subject}/{instance.resource_type}/{filename}"


class CourseResource(models.Model):
    RESOURCE_TYPES = (
        ('slide', '课件'),
        ('exercise', '练习'),
        ('reference', '参考资料'),
        ('other', '其他'),
    )

    course = models.ForeignKey(Course, related_name='course_resources_from_resources_app', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    file = models.FileField(upload_to=resource_upload_path)
    version = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True, null=True)
    # {{ edit_2 }}
    # created_by = models.ForeignKey(User, related_name='course_resources_created_in_resources_app', on_delete=models.CASCADE) # 移除创建者字段
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = '课程资源'
        verbose_name_plural = '课程资源管理'
        unique_together = [['course', 'title']]

    def __str__(self):
        return f"{self.title} (v{self.version})"

    def get_absolute_url(self):
        return reverse('resource-download', kwargs={'pk': self.pk})

    # 完善版本控制逻辑
    def create_new_version(self, file): # {{ edit_3 }} 移除 user 参数
        # 生成唯一文件名避免冲突
        filename = f"{self.title}_v{self.version + 1}{os.path.splitext(file.name)[1]}"
        new_file = default_storage.save(resource_upload_path(self, filename), file)

        return CourseResource.objects.create(
            course=self.course,
            title=self.title,
            resource_type=self.resource_type,
            file=new_file,
            version=self.version + 1,
            description=self.description,
            # created_by=user # {{ edit_4 }} 移除 created_by 参数
        )


class ResourceCollection(models.Model):
    """资源集合（用于导出）"""
    name = models.CharField(max_length=200)
    resources = models.ManyToManyField(CourseResource)
    # {{ edit_5 }}
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE) # 移除创建者字段
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# 优化文件删除信号处理，兼容云存储
@receiver(models.signals.post_delete, sender=CourseResource)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        try:
            instance.file.delete(save=False)
        except Exception as e:
            logger.error(f"删除资源文件失败: {str(e)}")

@receiver(models.signals.pre_save, sender=CourseResource)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old_file = CourseResource.objects.get(pk=instance.pk).file
    except CourseResource.DoesNotExist:
        return
    new_file = instance.file
    if old_file and old_file != new_file:
        try:
            old_file.delete(save=False)
        except Exception as e:
            logger.error(f"删除旧文件失败: {str(e)}")
