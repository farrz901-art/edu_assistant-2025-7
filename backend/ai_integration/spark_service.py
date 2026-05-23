## ai_integration/spark_service.py
import time
import hashlib
import logging
import json
import threading
from django.core.cache import cache
from django.conf import settings
from .prompt_templates import PROMPT_TEMPLATES
from utils.spark_api import SparkAPI  # WebSocket版本
# from utils.spark_http import SparkHTTP  # HTTP版本
from shared.exceptions import AIRequestError

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self, user_id=None, use_websocket=True):
        self.user_id = user_id
        self.domain = "education"

        if use_websocket:
            self.spark = SparkAPI(
                app_id=settings.SPARK_APPID,
                api_key=settings.SPARK_APIKEY,
                api_secret=settings.SPARK_APISECRET,
                domain=self.domain
            )
        else:
            # 使用HTTP版本
            from utils.spark_http import SparkHTTP
            self.spark = SparkHTTP(
                settings.SPARK_APPID,
                settings.SPARK_APIKEY,
                settings.SPARK_APISECRET,
                domain=self.domain
            )

    def _generate_cache_key(self, prompt_type, **kwargs):
        """生成唯一的缓存键"""
        params_str = json.dumps(kwargs, sort_keys=True)
        return f"ai_cache:{self.user_id}:{prompt_type}:{hashlib.md5(params_str.encode()).hexdigest()}"

    def _call_with_retry(self, func, *args, **kwargs):
        """带重试机制的API调用"""
        max_retries = settings.AI_MAX_RETRIES
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except AIRequestError as e:
                logger.warning(f"AI请求失败，尝试 {attempt + 1}/{max_retries}: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # 指数退避
                else:
                    raise
            except Exception as e:
                logger.error(f"AI请求未预期错误: {str(e)}")
                raise AIRequestError(f"AI服务错误: {str(e)}")

    def generate_course_content(self, subject, syllabus, total_hours=40):
        """生成教学内容"""
        cache_key = self._generate_cache_key(
            'course_design',
            subject=subject,
            syllabus=syllabus[:200],
            hours=total_hours
        )

        # 检查缓存
        if cached := cache.get(cache_key):
            return cached

        # 使用模板构建提示词
        prompt = PROMPT_TEMPLATES['course_design'].format(
            subject=subject,
            syllabus=syllabus,
            total_hours=total_hours
        )

        # 添加个性化上下文
        context = f"\n### 个性化要求:\n教师ID: {self.user_id}" if self.user_id else ""

        try:
            content = self._call_with_retry(
                self.spark.generate_teaching_content,
                syllabus=prompt,
                context=context
            )

            # 缓存结果（24小时）
            cache.set(cache_key, content, timeout=86400)
            return content
        except AIRequestError as e:
            logger.error(f"生成教学内容失败: {str(e)}")
            return (
                "教学内容生成失败。可能原因：\n"
                "1. AI服务暂时不可用\n"
                "2. 输入内容过于复杂\n"
                "3. 网络连接问题\n\n"
                "请稍后重试或简化课程大纲。"
            )

    def generate_exam_questions(self, content, question_types="选择题,简答题,编程题"):
        """生成考核题目"""
        cache_key = self._generate_cache_key(
            'exam_generation',
            content=content[:200],
            types=question_types
        )

        if cached := cache.get(cache_key):
            return cached

        # 使用模板构建提示词
        prompt = PROMPT_TEMPLATES['exam_generation'].format(
            content=content,
            question_types=question_types
        )

        try:
            questions = self._call_with_retry(
                self.spark.generate_exam_questions,
                content=prompt,
                question_types=question_types
            )

            # 尝试解析JSON（如果API返回JSON）
            try:
                parsed = json.loads(questions)
                cache.set(cache_key, parsed, timeout=3600)  # 缓存1小时
                return parsed
            except json.JSONDecodeError:
                cache.set(cache_key, questions, timeout=3600)
                return questions
        except AIRequestError as e:
            logger.error(f"生成考核题目失败: {str(e)}")
            return {"error": "题目生成失败，请稍后重试"}

    def answer_question(self, question, course_content):
        """回答学生问题"""
        # 限制上下文长度（优化性能）
        context = course_content[:3000] if course_content else ""

        try:
            return self._call_with_retry(
                self.spark.answer_student_question,
                question=question,
                course_content=context
            )
        except AIRequestError as e:
            logger.error(f"回答学生问题失败: {str(e)}")
            return "抱歉，暂时无法回答这个问题，请稍后再试。"

    def evaluate_answer(self, question, reference_answer, student_answer):
        """评估学生答案"""
        try:
            evaluation = self._call_with_retry(
                self.spark.evaluate_student_answer,
                question=question,
                reference_answer=reference_answer,
                student_answer=student_answer
            )

            # 尝试解析JSON
            try:
                return json.loads(evaluation)
            except json.JSONDecodeError:
                return {"score": 0, "feedback": evaluation}
        except AIRequestError as e:
            logger.error(f"评估答案失败: {str(e)}")
            return {
                "score": -1,
                "feedback": "评估失败，请稍后再试",
                "error": str(e)
            }

    def generate_practice_questions(self, student_level, topic, count=5):
        """生成练习题"""
        prompt = (
            f"为{student_level}水平的学生生成{topic}相关的练习题：\n"
            f"### 要求:\n"
            f"1. 生成{count}道题\n"
            f"2. 难度适合{student_level}水平\n"
            f"3. 包含多种题型\n"
            f"4. 使用JSON格式输出"
        )

        try:
            questions = self._call_with_retry(
                self.spark._send_request,
                messages=[{"role": "user", "content": prompt}]
            )

            try:
                return json.loads(questions)
            except json.JSONDecodeError:
                return questions
        except AIRequestError as e:
            logger.error(f"生成练习题失败: {str(e)}")
            return []
