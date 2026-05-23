import base64
import hashlib
import hmac
import json
import time
import websocket
import ssl
import threading
from urllib.parse import urlparse
from datetime import datetime
from time import mktime
from django.conf import settings
from wsgiref.handlers import format_date_time
from shared.exceptions import AIRequestError


class SparkAPI:
    def __init__(self, app_id, api_key, api_secret, domain="education", temperature=0.5, max_tokens=4096):
        self.app_id = app_id
        self.api_key = api_key
        self.api_secret = api_secret
        self.domain = domain
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.host = "spark-api.xf-yun.com"
        self.version = "v3.1"
        self.timeout = settings.AI_REQUEST_TIMEOUT

    def _generate_auth_url(self):
        """生成带鉴权参数的WebSocket URL"""
        date = format_date_time(mktime(datetime.now().timetuple()))

        # 拼接签名字符串
        signature_origin = f"host: {self.host}\ndate: {date}\nGET /{self.version}/chat HTTP/1.1"

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

        # 拼接URL
        return (
            f"wss://{self.host}/{self.version}/chat?authorization={authorization}"
            f"&date={date}&host={self.host}"
        )

    def _construct_request(self, messages):
        """构建API请求数据"""
        return {
            "header": {
                "app_id": self.app_id,
                "uid": "user123"  # 可自定义用户ID
            },
            "parameter": {
                "chat": {
                    "domain": self.domain,
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens
                }
            },
            "payload": {
                "message": {
                    "text": messages
                }
            }
        }

    def _send_request(self, messages):
        """发送请求并获取完整响应"""
        url = self._generate_auth_url()
        response = {"content": "", "status": "init", "usage": None}
        lock = threading.Lock()
        ws = None

        def on_open(ws):
            """WebSocket连接打开时发送请求"""
            request_data = self._construct_request(messages)
            ws.send(json.dumps(request_data))

        def on_message(ws, message):
            """处理接收到的消息"""
            data = json.loads(message)
            with lock:
                # 处理文本内容
                if "text" in data["payload"]["choices"]:
                    for text in data["payload"]["choices"]["text"]:
                        response["content"] += text["content"]

                # 处理状态
                if "status" in data["header"]:
                    response["status"] = data["header"]["status"]

                # 处理使用情况
                if "usage" in data["payload"]:
                    response["usage"] = data["payload"]["usage"]

                # 如果状态为2，表示结束
                if data["header"]["status"] == 2:
                    ws.close()

        def on_error(ws, error):
            """处理错误"""
            with lock:
                response["status"] = "error"
                response["error"] = str(error)
                ws.close()

        def on_close(ws, close_status_code, close_msg):
            """连接关闭"""
            pass

        # 创建WebSocket连接
        ws = websocket.WebSocketApp(
            url,
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )

        # 在独立线程中运行WebSocket
        wst = threading.Thread(target=ws.run_forever, kwargs={"sslopt": {"cert_reqs": ssl.CERT_NONE}})
        wst.daemon = True
        wst.start()

        # 等待响应完成或超时
        start_time = time.time()
        while wst.is_alive():
            if time.time() - start_time > self.timeout:
                ws.close()
                raise AIRequestError("AI请求超时")
            time.sleep(0.1)

        # 检查最终状态
        if response["status"] == "error":
            raise AIRequestError(f"AI请求失败: {response.get('error', '未知错误')}")

        if not response["content"]:
            raise AIRequestError("AI未返回有效内容")

        return response["content"]

    # 以下是针对教学场景的专用方法
    def generate_teaching_content(self, syllabus, context=""):
        """生成教学内容"""
        prompt = (
            f"你是一位经验丰富的教师，请根据以下课程大纲设计教学内容：\n"
            f"### 课程大纲:\n{syllabus}\n\n"
            f"### 要求:\n"
            f"1. 包含知识讲解、实训练习和指导\n"
            f"2. 合理分配时间（总课时40小时）\n"
            f"3. 使用Markdown格式输出\n"
            f"4. 包含实际案例和应用场景\n"
            f"{context}"
        )
        return self._send_request([{"role": "user", "content": prompt}])

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
