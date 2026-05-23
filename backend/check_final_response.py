import os
import django
import json

# Set up Django environment  
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.courses.models import Course
from apps.courses.serializers import CourseSerializer

def check_final_response():
    """
    检查最终的API响应格式
    """
    print("=== 检查最终的API响应格式 ===")
    
    # 获取所有课程
    courses = Course.objects.all()
    print(f"数据库中的课程数量: {courses.count()}")
    
    # 使用序列化器序列化数据
    serializer = CourseSerializer(courses, many=True)
    serialized_data = serializer.data
    
    # 模拟CourseViewSet的list方法返回的格式
    api_response = {
        'count': len(serialized_data),
        'next': None,
        'previous': None,
        'results': serialized_data
    }
    
    print("API响应数据:")
    print(json.dumps(api_response, indent=2, ensure_ascii=False))
    
    # 检查前端需要的关键字段
    print("\n=== 前端关键字段检查 ===")
    if api_response['results']:
        for i, course in enumerate(api_response['results']):
            print(f"课程 {i+1}:")
            print(f"  - id: {course.get('id')}")
            print(f"  - name: '{course.get('name')}'")
            print(f"  - description: '{course.get('description')}'")
    else:
        print("❌ 没有课程数据")

if __name__ == "__main__":
    check_final_response() 