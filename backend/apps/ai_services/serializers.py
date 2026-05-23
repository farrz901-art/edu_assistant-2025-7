from rest_framework import serializers
from apps.analytics.models import ExerciseQuestion

class AskQuestionSerializer(serializers.Serializer):
    """AI问答请求序列化器"""
    question = serializers.CharField(required=True, help_text="问题内容")
    course_id = serializers.IntegerField(required=True, help_text="课程ID")

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseQuestion
        fields = '__all__' # 返回模型的所有字段，包括id

class EvaluationSerializer(serializers.Serializer):
    question_id = serializers.IntegerField(required=True)
    answer = serializers.CharField()

class CourseDesignSerializer(serializers.Serializer):
    """
    @class CourseDesignSerializer
    @brief 序列化器，用于课程设计请求的数据验证。
    """
    syllabus = serializers.CharField(
        min_length=20,
        error_messages={'min_length': '课程大纲内容过短，请提供更详细的信息。'}
    )
    knowledge_base_docs = serializers.CharField(
        required=False, 
        allow_blank=True, 
        help_text="可选的知识库文档内容"
    )
    # 可选高级参数
    temperature = serializers.FloatField(required=False, min_value=0.0, max_value=1.0, help_text="温度0-1")
    top_k = serializers.IntegerField(required=False, min_value=1, max_value=6, help_text="top_k 取样")

class AssessmentGeneratorSerializer(serializers.Serializer):
    """
    @class AssessmentGeneratorSerializer
    @brief 序列化器，用于考核内容生成请求的数据验证。
    """
    teaching_content = serializers.CharField(help_text="教学内容")
    temperature = serializers.FloatField(required=False, min_value=0.0, max_value=1.0)
    top_k = serializers.IntegerField(required=False, min_value=1, max_value=6)

class LearningDataAnalysisSerializer(serializers.Serializer):
    """
    @class LearningDataAnalysisSerializer
    @brief 序列化器，用于学情数据分析请求的数据验证。
    """
    student_practice_history = serializers.CharField(help_text="学生练习历史数据，可以是JSON字符串或其他格式")
    temperature = serializers.FloatField(required=False, min_value=0.0, max_value=1.0)
    top_k = serializers.IntegerField(required=False, min_value=1, max_value=6)
