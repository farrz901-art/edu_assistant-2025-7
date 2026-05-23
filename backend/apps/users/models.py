from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    # # 添加 app_label
    # class Meta:
    #     app_label = 'users'
    #     db_table = 'users_user'
    ROLE_CHOICES = (
        ('admin', _('管理员')),
        ('teacher', _('教师')),
        ('student', _('学生')),
    )

    # 解决反向关系冲突
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to...',
        verbose_name='groups'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user...',
        verbose_name='user permissions'
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student',
        verbose_name=_('角色')
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name=_('手机号')
    )
    department = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('院系')
    )

    class Meta:
        verbose_name = _('用户')
        verbose_name_plural = _('用户管理')
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_teacher(self):
        return self.role == 'teacher'

    @property
    def is_student(self):
        return self.role == 'student'

    @property
    def is_admin(self):
        return self.role == 'admin'
