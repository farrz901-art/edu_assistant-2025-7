# backend/apps/ai_services/views.py
from rest_framework.permissions import AllowAny # {{ edit_1 }} 更改为 AllowAny
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from shared.exceptions import handle_view_exception
from apps.courses.models import Course
from apps.analytics.models import (
    ExerciseQuestion,
    ExerciseSubmission,
    LearningAnalytics,
    QuestionHistory
)
from apps.analytics.models import LearningAnalytics, QuestionHistory
from .serializers import AskQuestionSerializer, QuestionSerializer, EvaluationSerializer, CourseDesignSerializer, AssessmentGeneratorSerializer, LearningDataAnalysisSerializer # 导入新的序列化器
from ai_integration.xf_spark import AIService
from django.shortcuts import get_object_or_404 # 导入 get_object_or_404
import logging
import requests
from requests.exceptions import ConnectionError

logger = logging.getLogger(__name__)

class AskQuestionAPIView(APIView):
    """
    通用问答接口
    - 接收课程ID和问题文本
    - 调用AI服务进行回答
    - 记录问题历史
    """
    permission_classes = [AllowAny]

    @handle_view_exception
    def post(self, request, *args, **kwargs):
        serializer = AskQuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        course_id = serializer.validated_data.get('course_id')
        question_text = serializer.validated_data.get('question')

        if not all([course_id, question_text]):
            raise ValidationError("必须提供 course_id 和 question。")

        course = get_object_or_404(Course, id=course_id)

        try:
            ai_service = AIService(user_id=request.user.id if request.user.is_authenticated else None)
            context = course.content[:5000] if course.content else ""
            answer = ai_service.answer_question(question_text, context)

            # 异步记录问题历史（如果需要）
            # record_question_history.delay(course_id, question_text, answer)

            QuestionHistory.objects.create(
                course=course,
                question=question_text,
                answer=answer
            )

            return Response({'answer': answer}, status=status.HTTP_200_OK)

        except (ConnectionError, requests.exceptions.ReadTimeout) as e:
            logger.error(f"调用AI问答服务时出错: {e}", exc_info=True)
            return Response(
                {"error": "抱歉，AI服务暂时无法连接或响应超时，请稍后再试。"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except Exception as e:
            logger.error(f"处理AI问答请求时发生未知错误: {e}", exc_info=True)
            return Response(
                {"error": "处理您的请求时发生内部错误。"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AnswerEvaluationAPIView(APIView):
    """
    答案评估接口
    使用AI评估学生答案
    """
    permission_classes = [AllowAny]

    @handle_view_exception
    def post(self, request):
        serializer = EvaluationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        question_id = serializer.validated_data['question_id']
        answer_text = serializer.validated_data['answer']

        try:
            question = get_object_or_404(ExerciseQuestion, id=question_id)
            ai_service = AIService(user_id=request.user.id if request.user.is_authenticated else None)

            evaluation = ai_service.evaluate_answer(
                question=question.text,
                reference_answer=question.reference_answer,
                student_answer=answer_text
            )

            ExerciseSubmission.objects.create(
                question=question,
                answer=answer_text,
                evaluation=evaluation
            )

            return Response(evaluation, status=status.HTTP_200_OK)

        except (ConnectionError, requests.exceptions.ReadTimeout) as e:
            logger.error(f"调用AI评估服务时出错: {e}", exc_info=True)
            return Response(
                {"error": "抱歉，AI评估服务暂时无法连接或响应超时，请稍后再试。"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except Exception as e:
            logger.error(f"处理答案评估请求时发生未知错误: {e}", exc_info=True)
            return Response(
                {"error": "处理您的请求时发生内部错误。"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PracticeGeneratorAPIView(APIView):
    permission_classes = [AllowAny]

    @handle_view_exception
    def post(self, request):
        topic = request.data.get('topic', '综合练习')
        count = request.data.get('count', 5)
        course_id = request.data.get('course_id')

        if not topic or not isinstance(count, int) or not (1 <= count <= 20):
            raise ValidationError('参数无效')

        try:
            ai_service = AIService(user_id=request.user.id if request.user.is_authenticated else None)
            generated_questions = ai_service.generate_practice_questions(
                topic=topic,
                count=count
            )

            course = get_object_or_404(Course, id=course_id) if course_id else None

            saved_questions = []
            for q_data in generated_questions:
                question = ExerciseQuestion.objects.create(
                    course=course,
                    topic=topic,
                    question_type=self._map_type_to_model(q_data.get('type', 'text')),
                    difficulty=q_data.get('difficulty', 'medium'),
                    text=q_data.get('text', ''),
                    options=q_data.get('options'),
                    reference_answer=q_data.get('answer', ''),
                    test_cases=q_data.get('test_cases')
                )
                saved_questions.append(question)

            serializer = QuestionSerializer(saved_questions, many=True)
            return Response({"questions": serializer.data}, status=status.HTTP_200_OK)

        except (ConnectionError, requests.exceptions.ReadTimeout) as e:
            logger.error(f"调用AI习题生成服务时出错: {e}", exc_info=True)
            return Response(
                {"error": "抱歉，AI习题生成服务暂时无法连接或响应超时，请稍后再试。", "questions": []},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except Exception as e:
            logger.error(f"处理习题生成请求时发生未知错误: {e}", exc_info=True)
            return Response(
                {"error": "处理您的请求时发生内部错误。"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _map_type_to_model(self, ai_type: str) -> str:
        """将AI返回的类型映射到模型choice"""
        ai_type = ai_type.lower()
        if '编程' in ai_type or 'code' in ai_type:
            return 'code'
        if '选择' in ai_type or 'choice' in ai_type:
            return 'choice'
        return 'text'


class CourseDesignAPIView(APIView):
    """
    @class CourseDesignAPIView
    @brief 教师备课与设计接口
    @details 根据课程大纲和知识库文档自动设计教学内容。
    """
    permission_classes = [AllowAny]

    @handle_view_exception
    def post(self, request):
        serializer = CourseDesignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        syllabus = serializer.validated_data['syllabus']
        knowledge_base_docs = serializer.validated_data['knowledge_base_docs']

        ai_service = AIService(user_id=None)
        designed_content = ai_service.design_course(syllabus, knowledge_base_docs)

        return Response({"designed_content": designed_content}, status=status.HTTP_200_OK)


class AssessmentGeneratorAPIView(APIView):
    """
    @class AssessmentGeneratorAPIView
    @brief 教师考核内容生成接口
    @details 根据教学内容自动生成考核题目及参考答案。
    """
    permission_classes = [AllowAny]

    @handle_view_exception
    def post(self, request):
        serializer = AssessmentGeneratorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        teaching_content = serializer.validated_data['teaching_content']

        ai_service = AIService(user_id=None)
        questions = ai_service.generate_assessment(teaching_content)

        return Response({"questions": questions}, status=status.HTTP_200_OK)


class LearningDataAnalysisAPIView(APIView):
    """
    @class LearningDataAnalysisAPIView
    @brief 教师学情数据分析接口
    @details 对学生提交的答案进行自动化检测，提供错误定位与修正建议；对学生整体数据进行分析，总结知识掌握情况与教学建议。
    """
    permission_classes = [AllowAny]

    @handle_view_exception
    def post(self, request):
        serializer = LearningDataAnalysisSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        student_practice_history = serializer.validated_data['student_practice_history']

        ai_service = AIService(user_id=None)
        analysis = ai_service.analyze_learning_data(student_practice_history)

        return Response(analysis, status=status.HTTP_200_OK)