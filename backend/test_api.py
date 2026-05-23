import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.courses.models import Course
from apps.courses.serializers import CourseSerializer

def test_course_api():
    """
    测试课程API和序列化器
    """
    print("=== 测试课程API ===")
    
    # 检查Course模型是否可用
    try:
        course_count = Course.objects.count()
        print(f"数据库中课程数量: {course_count}")
    except Exception as e:
        print(f"数据库访问错误: {e}")
        return
    
    # 如果没有课程，创建一些测试数据
    if course_count == 0:
        print("创建测试课程...")
        test_courses = [
            {
                'title': 'Python基础编程',
                'subject': '计算机科学',
                'syllabus': '学习Python编程语言的基础知识',
                'content': 'Python课程内容'
            },
            {
                'title': '数据结构与算法',
                'subject': '计算机科学', 
                'syllabus': '学习数据结构和算法',
                'content': '算法课程内容'
            }
        ]
        
        for course_data in test_courses:
            course = Course.objects.create(**course_data)
            print(f"创建课程: {course.title}")
    
    # 测试序列化器
    print("\n=== 测试序列化器 ===")
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    serialized_data = serializer.data
    
    print(f"序列化课程数量: {len(serialized_data)}")
    for course_data in serialized_data:
        print(f"课程: name='{course_data.get('name')}', description='{course_data.get('description')}'")

if __name__ == "__main__":
    test_course_api() 