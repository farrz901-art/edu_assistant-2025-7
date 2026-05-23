import os
import django
import json

# Set up Django environment  
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import RequestFactory
from apps.courses.views import CourseViewSet

def test_api_endpoint():
    """
    测试课程API端点是否返回正确的数据
    """
    print("=== 测试课程API端点 ===")
    
    # 创建一个模拟的GET请求
    factory = RequestFactory()
    request = factory.get('/api/courses/')
    
    # 创建视图集实例并调用list方法
    viewset = CourseViewSet()
    viewset.request = request
    
    try:
        response = viewset.list(request)
        response_data = response.data
        
        print(f"API响应状态码: {response.status_code}")
        print(f"API响应数据: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
        
        if 'results' in response_data and len(response_data['results']) > 0:
            print("✅ API返回了课程数据")
            for course in response_data['results']:
                print(f"   - 课程: {course.get('name', 'N/A')} | 描述: {course.get('description', 'N/A')}")
        else:
            print("❌ API没有返回课程数据")
            
    except Exception as e:
        print(f"❌ API调用失败: {e}")

if __name__ == "__main__":
    test_api_endpoint() 