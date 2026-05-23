import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.courses.models import Course

def create_test_courses():
    """
    创建一些测试课程数据
    """
    courses_data = [
        {
            'title': 'Python基础编程',
            'subject': '计算机科学',
            'syllabus': '学习Python编程语言的基础知识，包括变量、函数、类等概念。',
            'content': '这是Python基础编程课程的详细内容。'
        },
        {
            'title': '数据结构与算法',
            'subject': '计算机科学',
            'syllabus': '学习常用的数据结构和算法，提高编程能力和解决问题的思维。',
            'content': '这是数据结构与算法课程的详细内容。'
        },
        {
            'title': 'Web开发入门',
            'subject': '计算机科学',
            'syllabus': '学习HTML、CSS、JavaScript等前端技术，以及后端开发基础。',
            'content': '这是Web开发入门课程的详细内容。'
        }
    ]
    
    created_count = 0
    for course_data in courses_data:
        course, created = Course.objects.get_or_create(
            title=course_data['title'],
            defaults=course_data
        )
        if created:
            created_count += 1
            print(f"创建课程: {course.title}")
        else:
            print(f"课程已存在: {course.title}")
    
    print(f"总共创建了 {created_count} 门新课程")
    print(f"数据库中总课程数: {Course.objects.count()}")

if __name__ == "__main__":
    create_test_courses() 