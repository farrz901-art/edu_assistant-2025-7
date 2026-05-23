#!/usr/bin/env python3
"""
调试考核内容生成功能
"""
import os
import sys
import django
import json
import logging

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from ai_integration.xf_spark import AIService, _clean_json_content

def debug_assessment_generation():
    """调试考核内容生成"""
    print("🔍 开始调试考核内容生成...")
    
    # 使用简短的教学内容
    teaching_content = "二元一次函数的形式为：z=ax+by+c，其中a、b、c是常数。"
    
    ai_service = AIService()
    
    # 构建消息
    messages = [
        {
            "role": "system", 
            "content": "你是一名教师，请根据教学内容生成2道考核题目。必须返回JSON数组格式。"
        },
        {
            "role": "user", 
            "content": f"教学内容：{teaching_content}"
        }
    ]
    
    try:
        print("📡 调用AI服务...")
        raw_response = ai_service._call_chat(messages)
        
        print(f"📏 原始响应长度: {len(raw_response)} 字符")
        print(f"📄 响应开头: {raw_response[:200]}...")
        print(f"📄 响应结尾: ...{raw_response[-200:]}")
        
        # 检查是否被截断
        if not raw_response.strip().endswith(']') and not raw_response.strip().endswith('}'):
            print("⚠️  警告：响应似乎被截断了！")
        
        # 尝试清理
        print("\n🧹 清理响应内容...")
        cleaned = _clean_json_content(raw_response)
        print(f"清理后长度: {len(cleaned)} 字符")
        
        # 尝试解析JSON
        print("\n📊 尝试解析JSON...")
        try:
            parsed = json.loads(cleaned)
            print(f"✅ JSON解析成功！")
            print(f"   类型: {type(parsed)}")
            if isinstance(parsed, list):
                print(f"   题目数量: {len(parsed)}")
                for i, q in enumerate(parsed):
                    print(f"   题目{i+1}: {q.get('text', 'N/A')[:50]}...")
            return parsed
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            print(f"   错误位置: 第{e.lineno}行, 第{e.colno}列")
            
            # 尝试修复常见问题
            print("\n🔧 尝试修复JSON...")
            if cleaned.count('[') > cleaned.count(']'):
                fixed = cleaned + ']'
                try:
                    parsed = json.loads(fixed)
                    print("✅ 修复成功！添加了缺失的']'")
                    return parsed
                except:
                    pass
            
            print("❌ 修复失败")
            return []
            
    except Exception as e:
        print(f"❌ 调用AI服务失败: {e}")
        return []

def test_simple_request():
    """测试最简单的请求"""
    print("\n🧪 测试最简单的请求...")
    
    ai_service = AIService()
    messages = [
        {"role": "user", "content": "请生成1道关于数学的选择题，返回JSON格式"}
    ]
    
    try:
        response = ai_service._call_chat(messages)
        print(f"简单请求响应: {response[:300]}...")
        return len(response) > 0
    except Exception as e:
        print(f"简单请求失败: {e}")
        return False

if __name__ == "__main__":
    # 测试简单请求
    if test_simple_request():
        print("✅ AI服务基础功能正常")
    else:
        print("❌ AI服务基础功能异常")
        sys.exit(1)
    
    # 调试考核内容生成
    result = debug_assessment_generation()
    
    if result:
        print(f"\n🎉 成功生成 {len(result)} 道题目")
    else:
        print("\n💥 考核内容生成失败") 