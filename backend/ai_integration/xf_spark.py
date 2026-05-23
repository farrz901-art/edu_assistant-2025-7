"""xf_spark.py
讯飞星火认知大模型 HTTP API 封装
文档参考: https://www.xfyun.cn/doc/spark/HTTP%E8%B0%83%E7%94%A8%E6%96%87%E6%A1%A3.html
"""
from __future__ import annotations

import os
import uuid
import json
import logging
from typing import List, Dict, Any
from django.core.exceptions import ImproperlyConfigured

import requests

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# 环境变量读取
# ---------------------------------------------------------------------------
SPARK_API_BASE = os.getenv("SPARK_API_BASE", "https://spark-api-open.xf-yun.com/v1")
SPARK_API_ENDPOINT = f"{SPARK_API_BASE}/chat/completions"
# 使用SPARK_API_PASSWORD进行HTTP API认证
SPARK_API_PASSWORD = os.getenv("SPARK_API_PASSWORD", "")
# WebSocket API相关配置（备用）
SPARK_APP_ID = os.getenv("SPARK_APP_ID", "")
SPARK_API_SECRET = os.getenv("SPARK_API_SECRET", "")
SPARK_API_KEY = os.getenv("SPARK_API_KEY", "")
DEFAULT_MODEL = os.getenv("SPARK_MODEL", "generalv3.5")

if not SPARK_API_PASSWORD:
    logger.warning("[XFSpark] SPARK_API_PASSWORD not set. API calls will fail.")

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {SPARK_API_PASSWORD}",
}


# ---------------------------------------------------------------------------
# 帮助函数
# ---------------------------------------------------------------------------

def _call_chat(messages: List[Dict[str, str]], model: str = DEFAULT_MODEL, **extra) -> str:
    """向讯飞星火接口发送对话请求并返回content字符串。"""
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
    }
    payload.update(extra)

    try:
        resp = requests.post(
            SPARK_API_ENDPOINT,
            headers=HEADERS,
            data=json.dumps(payload),
            timeout=120,
        )
        resp.raise_for_status()
        data = resp.json()
        # 按照星火返回格式提取content
        return data["choices"][0]["message"]["content"]
    except Exception as exc:
        logger.exception("[XFSpark] request failed: %s", exc)
        raise


def _clean_json_content(content: str) -> str:
    """清理AI返回的内容，去除markdown代码块包裹"""
    content = content.strip()
    if content.startswith("```json") and content.endswith("```"):
        return content[7:-3].strip()
    elif content.startswith("```") and content.endswith("```"):
        return content[3:-3].strip()
    return content


# ---------------------------------------------------------------------------
# 高层封装类
# ---------------------------------------------------------------------------

class AIService:
    """高层AI服务封装，接口与旧 spark_service 兼容。"""

    def __init__(self, user_id: str | None = None, model: str | None = None):
        """
        初始化AI服务，并严格校验所需的环境变量。
        """
        self.spark_api_password = os.getenv("SPARK_API_PASSWORD")
        if not self.spark_api_password:
            raise ImproperlyConfigured(
                "环境变量 SPARK_API_PASSWORD 未设置。请检查您的 .env 文件或容器环境配置。"
            )

        self.api_base = os.getenv("SPARK_API_BASE", "https://spark-api-open.xf-yun.com/v1")
        self.endpoint = f"{self.api_base}/chat/completions"
        self.model = model or os.getenv("SPARK_MODEL", "generalv3.5")
        self.user_id = user_id or str(uuid.uuid4())
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.spark_api_password}",
        }

    def _call_chat(self, messages: List[Dict[str, str]], **extra) -> str:
        """向讯飞星火接口发送对话请求并返回content字符串。"""
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
        }
        payload.update(extra)

        try:
            resp = requests.post(
                self.endpoint,
                headers=self.headers,
                data=json.dumps(payload),
                timeout=120,
            )
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        except Exception as exc:
            logger.exception("[XFSpark] 请求失败: %s", exc)
            # 将底层异常重新包装为更具体的业务异常
            raise ConnectionError(f"AI服务请求失败: {exc}") from exc

    # ------------------------ 学生端 ------------------------
    def answer_question(self, question: str, context: str = "", **extra) -> str:
        messages = [
            {"role": "system", "content": "你是一名专业教师，请根据提供的课程内容回答学生问题。"},
            {"role": "user", "content": f"课程内容: {context}\n学生问题: {question}"},
        ]
        return self._call_chat(messages, user=self.user_id, **extra)

    def generate_practice_questions(self, topic: str, count: int = 5, **extra) -> List[Dict[str, Any]]:
        # 使用Few-shot示例来引导AI返回更精确的格式
        example_request = "主题: Python列表推导式\n请生成数量: 1"
        example_response = """
        [
            {
                "type": "编程题",
                "difficulty": "medium",
                "text": "给定一个数字列表，请使用列表推导式创建一个新列表，其中仅包含原始列表中的偶数。",
                "answer": "[num for num in old_list if num % 2 == 0]",
                "explanation": "列表推导式提供了一种简洁的创建列表的方法。这个表达式遍历`old_list`，并对每个`num`执行`if num % 2 == 0`的条件判断，只有满足条件的元素才会被包含在新列表中。"
            }
        ]
        """
        messages = [
            {"role": "system", "content": "你是一名出题专家。请严格按照用户要求的格式和数量生成练习题。编程题的type必须是'编程题'。"},
            {"role": "user", "content": example_request},
            {"role": "assistant", "content": example_response},
            {"role": "user", "content": f"主题: {topic}\n请生成数量: {count}"},
        ]
        content = self._call_chat(messages, user=self.user_id, **extra)
        try:
            content = _clean_json_content(content)
            return json.loads(content)
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse JSON from AI response: {content[:200]}...")
            return []

    def evaluate_answer(self, question: str, reference_answer: str, student_answer: str, **extra) -> Dict[str, Any]:
        messages = [
            {"role": "system", "content": "你是一名AI评测助教，请对学生答案进行评分(0-10)、给出反馈及改进建议，返回JSON {score:int, feedback:str, suggestions:[str]}。"},
            {"role": "user", "content": f"题目: {question}\n参考答案: {reference_answer}\n学生答案: {student_answer}"},
        ]
        content = self._call_chat(messages, user=self.user_id, **extra)
        try:
            content = _clean_json_content(content)
            return json.loads(content)
        except json.JSONDecodeError:
            return {"score": 0, "feedback": "解析失败", "suggestions": []}

    # ------------------------ 教师端 ------------------------
    def design_course(self, syllabus: str, knowledge_base_docs: str = "", **extra) -> Dict[str, str]:
        # 使用Few-shot示例来引导AI返回更精确的JSON格式
        example_request = "课程大纲: Python基础-变量与数据类型"
        example_response = """
        {
            "knowledge_explanation": "1. **变量**: 在Python中，变量是用来存储数据的容器...\\n2. **数据类型**: 主要有整数(int), 浮点数(float), 字符串(str)...",
            "practical_exercises": "1. 声明一个名为`name`的变量并赋值为你的名字。\\n2. 计算两个整数的和并打印结果。",
            "time_distribution": "知识讲解: 25分钟, 实训练习: 15分钟, 问答环节: 5分钟"
        }
        """
        messages = [
            {"role": "system", "content": "你是一名课程设计专家，请严格根据大纲和知识库文档输出JSON对象，格式为 {\"knowledge_explanation\": \"...\", \"practical_exercises\": \"...\", \"time_distribution\": \"...\"}。"},
            {"role": "user", "content": example_request},
            {"role": "assistant", "content": example_response},
            {"role": "user", "content": f"课程大纲: {syllabus}\n知识库文档: {knowledge_base_docs}"},
        ]
        content = self._call_chat(messages, user=self.user_id, **extra)
        try:
            content = _clean_json_content(content)
            return json.loads(content)
        except json.JSONDecodeError:
            # 如果解析失败，将整个返回内容作为知识讲解，并记录警告
            logger.warning(f"Failed to parse JSON from design_course, returning content as fallback: {content[:200]}...")
            return {
                "knowledge_explanation": content,
                "practical_exercises": "AI返回格式有误，请尝试优化输入或重试。",
                "time_distribution": "AI返回格式有误，请尝试优化输入或重试。"
            }

    def generate_assessment(self, teaching_content: str, **extra) -> List[Dict[str, Any]]:
        # 使用更简洁的提示，减少响应长度
        messages = [
            {"role": "system", "content": "你是出题专家。请根据教学内容生成2道考核题。严格返回JSON数组格式：[{\"type\":\"选择题\",\"text\":\"题目内容\",\"answer\":\"答案\"}]"},
            {"role": "user", "content": f"教学内容：{teaching_content[:200]}..."},  # 限制输入长度
        ]
        content = self._call_chat(messages, user=self.user_id, **extra)
        try:
            content = _clean_json_content(content)
            
            # 尝试修复截断的JSON
            if content.count('[') > content.count(']'):
                content = content + ']'
            if content.count('{') > content.count('}'):
                content = content + '}'
                
            data = json.loads(content)
            
            # 处理字段名映射
            normalized_data = []
            for item in data:
                if isinstance(item, dict):
                    normalized_item = {
                        'type': item.get('type', item.get('类型', '选择题')),
                        'text': item.get('text', item.get('题目', item.get('question', ''))),
                        'answer': item.get('answer', item.get('答案', ''))
                    }
                    if normalized_item['text']:  # 只添加有内容的题目
                        normalized_data.append(normalized_item)
            
            return normalized_data
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON from generate_assessment: {content[:200]}... Error: {e}")
            # 返回一个备用题目
            return [{
                'type': '文字题',
                'text': f'请根据以下内容回答问题：{teaching_content[:100]}...',
                'answer': '请根据教学内容回答'
            }]

    def analyze_learning_data(self, student_practice_history: str, **extra) -> Dict[str, Any]:
        # 使用Few-shot示例来引导AI返回更精确的JSON格式
        example_request = """
[
  { "student_id": "001", "question": "Python的GIL是什么？", "answer": "全局解释器锁", "score": 9},
  { "student_id": "002", "question": "Python的GIL是什么？", "answer": "不知道", "score": 1}
]
"""
        example_response = """
{
    "knowledge_mastery_summary": "大部分学生对GIL（全局解释器锁）有基本概念，但理解深度不足。核心掌握点：1. CPython特有；2. 限制多线程并行。薄弱点：1. GIL对CPU密集型与I/O密集型任务的不同影响；2. 为何存在GIL。",
    "teaching_suggestions": [
        "建议补充讲解GIL的历史背景和设计初衷。",
        "可以设计一个对比实验，分别运行CPU密集型和I/O密集型代码，让学生直观感受GIL的影响。",
        "引导学生思考在什么场景下应该使用多线程，什么场景下使用多进程或异步IO。"
    ]
}
"""
        messages = [
            {"role": "system", "content": "你是一名教学数据分析师，请根据学生练习历史输出JSON对象，格式为 {\"knowledge_mastery_summary\": \"...\", \"teaching_suggestions\": [\"...\"]}。总结必须提炼出学生掌握的核心点和普遍存在的薄弱点。"},
            {"role": "user", "content": example_request},
            {"role": "assistant", "content": example_response},
            {"role": "user", "content": student_practice_history},
        ]
        content = self._call_chat(messages, user=self.user_id, **extra)
        try:
            content = _clean_json_content(content)
            return json.loads(content)
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse JSON from analyze_learning_data, returning content as fallback: {content[:200]}...")
            return {
                "knowledge_mastery_summary": "AI返回格式有误，请尝试优化输入或重试。",
                "teaching_suggestions": [content]
            } 