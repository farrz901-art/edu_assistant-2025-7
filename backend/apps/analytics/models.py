# apps/analytics/models.py
from django.db import models
# {{ edit_1 }}
# from apps.users.models import User # 移除 User 模型的导入
from apps.courses.models import Course


class LearningAnalytics(models.Model):
    # 添加level字段
    LEVEL_CHOICES = (
        ('beginner', '初级'),
        ('intermediate', '中级'),
        ('advanced', '高级'),
    )
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')

    def update_analytics(self, new_result):
        self.completion_rate = self._calculate_completion(new_result)
        self.accuracy_rate = self._calculate_accuracy(new_result)
        self.weak_topics = self._identify_weak_topics(new_result)
        self.save()

        # 更新用户等级
        if self.accuracy_rate > 80:
            self.level = 'advanced'
        elif self.accuracy_rate > 60:
            self.level = 'intermediate'
        else:
            self.level = 'beginner'
        self.save(update_fields=['level'])


    def _calculate_completion(self, result):
        """计算完成率逻辑"""
        # 示例实现：根据新结果更新完成率
        total_items = result.get('total_items', 1)
        completed_items = result.get('completed_items', 0)
        return (completed_items / total_items) * 100 if total_items > 0 else 0

    def _calculate_accuracy(self, result):
        """计算正确率逻辑"""
        # 示例实现：根据新结果更新正确率
        total_questions = result.get('total_questions', 1)
        correct_answers = result.get('correct_answers', 0)
        return (correct_answers / total_questions) * 100 if total_questions > 0 else 0

    def _identify_weak_topics(self, result):
        """识别薄弱知识点逻辑"""
        # 示例实现：根据错误率识别薄弱知识点
        weak_topics = []
        for topic, stats in result.get('topic_stats', {}).items():
            if stats.get('accuracy', 0) < 60:  # 正确率低于60%视为薄弱
                weak_topics.append(topic)
        return weak_topics

class QuestionHistory(models.Model):
    # {{ edit_2 }}
    # student = models.ForeignKey(User, on_delete=models.CASCADE) # 移除 student 字段
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class UserActivityLog(models.Model):
    # {{ edit_3 }}
    # user = models.ForeignKey(User, on_delete=models.CASCADE) # 移除 user 字段
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

class ExerciseQuestion(models.Model):
    """
    练习题目表
    """
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="关联课程")
    topic = models.CharField(max_length=200, default="综合练习", verbose_name="所属主题")
    question_type = models.CharField(max_length=50, choices=[
        ('text', '文字题'),
        ('choice', '选择题'),
        ('code', '编程题')
    ], verbose_name="题目类型")
    difficulty = models.CharField(max_length=20, default='medium', choices=[
        ('easy', '简单'),
        ('medium', '中等'),
        ('hard', '困难')
    ], verbose_name="难度")
    text = models.TextField(verbose_name="题干")
    options = models.JSONField(null=True, blank=True, verbose_name="选项")
    reference_answer = models.TextField(verbose_name="参考答案")
    test_cases = models.JSONField(null=True, blank=True, verbose_name="测试用例")

    def __str__(self):
        return f"[{self.get_question_type_display()}] {self.text[:30]}..."

class ExerciseSubmission(models.Model):
    """练习提交模型"""
    # {{ edit_4 }}
    # student = models.ForeignKey(User, on_delete=models.CASCADE) # 移除 student 字段
    question = models.ForeignKey(ExerciseQuestion, on_delete=models.CASCADE)
    answer = models.TextField()
    evaluation = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

class ExerciseHistory(models.Model):
    """练习历史模型"""
    # {{ edit_5 }}
    # student = models.ForeignKey(User, on_delete=models.CASCADE) # 移除 student 字段
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)