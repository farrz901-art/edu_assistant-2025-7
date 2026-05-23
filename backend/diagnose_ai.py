#!/usr/bin/env python3
"""
AI服务诊断脚本
"""
import requests
import json
import os

def test_connection():
    """测试讯飞API连接"""
    print("🔍 正在诊断AI服务连接...")
    
    # 检查环境变量
    api_password = os.getenv("SPARK_API_PASSWORD", "jtPbAuJWdwfvfPdxZhot:MSnKdGJqnETWfswICYLw")
    api_base = "https://spark-api-open.xf-yun.com/v1"
    endpoint = f"{api_base}/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_password}",
    }
    
    payload = {
        "model": "generalv3.5",
        "messages": [
            {"role": "user", "content": "简单回答：1+1等于几？"}
        ],
        "stream": False,
    }
    
    try:
        print(f"📡 正在连接: {endpoint}")
        response = requests.post(
            endpoint,
            headers=headers,
            data=json.dumps(payload),
            timeout=30
        )
        
        print(f"📊 状态码: {response.status_code}")
        print(f"📏 响应长度: {len(response.text)} 字符")
        
        if response.status_code == 200:
            try:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                print(f"✅ AI回答: {content}")
                return True
            except (KeyError, json.JSONDecodeError) as e:
                print(f"❌ JSON解析错误: {e}")
                print(f"原始响应: {response.text[:500]}...")
        else:
            print(f"❌ API请求失败: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 连接失败: {e}")
        
    return False

def test_simple_generation():
    """测试简单的内容生成"""
    print("\n🧪 测试内容生成...")
    
    try:
        # 尝试在容器内测试
        import sys
        sys.path.append('/app')
        
        from ai_integration.xf_spark import AIService
        
        ai_service = AIService()
        
        # 测试简单问答
        print("测试1: 简单问答")
        answer = ai_service.answer_question("什么是Python？", "Python是一种编程语言")
        print(f"✅ 问答测试成功: {answer[:100]}...")
        
        # 测试题目生成
        print("\n测试2: 题目生成")
        questions = ai_service.generate_practice_questions("Python基础", 1)
        print(f"📝 生成题目数量: {len(questions)}")
        if questions:
            print(f"✅ 题目生成成功: {questions[0].get('text', 'N/A')[:100]}...")
        else:
            print("❌ 题目生成失败")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    # 基础连接测试
    if test_connection():
        print("\n🎉 基础连接测试通过")
    else:
        print("\n💥 基础连接测试失败")
    
    # 服务集成测试
    test_simple_generation() 