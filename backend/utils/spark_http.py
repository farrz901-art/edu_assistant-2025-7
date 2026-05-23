# utils/spark_http.py
import base64
import hashlib
import hmac
import json
import requests
from datetime import datetime
from time import mktime
from wsgiref.handlers import format_date_time
from shared.exceptions import AIRequestError


class SparkHTTP:
    def __init__(self, app_id, api_key, api_secret, domain="general"):
        self.app_id = app_id
        self.api_key = api_key
        self.api_secret = api_secret
        self.domain = domain
        self.host = "spark-api.xf-yun.com"
        self.version = "v3.1"
        self.base_url = f"https://{self.host}/{self.version}/chat"
        self.timeout = 30

    def _generate_auth_header(self):
        """生成鉴权Header"""
        date = format_date_time(mktime(datetime.now().timetuple()))

        # 拼接签名字符串
        signature_origin = f"host: {self.host}\ndate: {date}\nPOST /{self.version}/chat HTTP/1.1"

        # 进行hmac-sha256加密
        signature_sha = hmac.new(
            self.api_secret.encode('utf-8'),
            signature_origin.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()

        # Base64编码
        signature_sha_base64 = base64.b64encode(signature_sha).decode('utf-8')

        # 拼接授权参数
        authorization_origin = (
            f'api_key="{self.api_key}", algorithm="hmac-sha256", '
            f'headers="host date request-line", signature="{signature_sha_base64}"'
        )

        # Base64编码授权参数
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode('utf-8')

        return {
            "Authorization": authorization,
            "Host": self.host,
            "Date": date,
            "Content-Type": "application/json"
        }

    def send_request(self, messages):
        """发送HTTP请求"""
        headers = self._generate_auth_header()
        payload = {
            "header": {
                "app_id": self.app_id,
                "uid": "user123"
            },
            "parameter": {
                "chat": {
                    "domain": self.domain,
                    "temperature": 0.5,
                    "max_tokens": 4096
                }
            },
            "payload": {
                "message": {
                    "text": messages
                }
            }
        }

        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                data=json.dumps(payload),
                timeout=self.timeout
            )
            response.raise_for_status()

            data = response.json()
            if data["header"]["code"] != 0:
                raise AIRequestError(f"AI请求失败: {data['header']['message']}")

            # 拼接所有文本内容
            content = ""
            for text in data["payload"]["choices"]["text"]:
                content += text["content"]

            return content

        except requests.exceptions.RequestException as e:
            raise AIRequestError(f"HTTP请求失败: {str(e)}")

    # 教学专用方法（与WebSocket版本一致）
    def generate_teaching_content(self, syllabus, context=""):
        """生成教学内容"""
        prompt = ...  # 与WebSocket版本相同
        return self.send_request([{"role": "user", "content": prompt}])

    # 其他方法实现与WebSocket版本相同
    def generate_exam_questions(self, content, question_types="选择题,简答题,编程题", context=""):
        """生成考核题目"""
        prompt = (
            f"根据以下教学内容生成考核题目：\n"
            f"### 教学内容:\n{content}\n\n"
            f"### 要求:\n"
            f"1. 生成5道题目，包含{question_types}\n"
            f"2. 编程题需提供测试用例\n"
            f"3. 每题附带参考答案和解析\n"
            f"4. 使用JSON格式输出\n"
            f"{context}"
        )
        return self._send_request([{"role": "user", "content": prompt}])

    def answer_student_question(self, question, course_content, context=""):
        """回答学生问题"""
        prompt = (
            f"你是一位课程助教，请基于以下课程内容回答学生问题：\n"
            f"### 课程内容:\n{course_content[:2000]}\n\n"  # 限制上下文长度
            f"### 学生问题:\n{question}\n\n"
            f"### 要求:\n"
            f"1. 回答简洁明了，不超过300字\n"
            f"2. 适当使用示例说明\n"
            f"3. 如果问题超出课程范围，礼貌提示\n"
            f"{context}"
        )
        return self._send_request([{"role": "user", "content": prompt}])

    def evaluate_student_answer(self, question, reference_answer, student_answer, context=""):
        """评估学生答案"""
        prompt = (
            f"请评估学生的答案：\n"
            f"### 题目:\n{question}\n\n"
            f"### 参考答案:\n{reference_answer}\n\n"
            f"### 学生答案:\n{student_answer}\n\n"
            f"### 要求:\n"
            f"1. 给出评分（0-10分）\n"
            f"2. 指出错误和不足\n"
            f"3. 提供改进建议\n"
            f"4. 使用JSON格式输出\n"
            f"{context}"
        )
        return self._send_request([{"role": "user", "content": prompt}])
