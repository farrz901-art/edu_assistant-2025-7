import os
import django

# Set up Django environment  
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.courses.models import Course

def restore_courses():
    """恢复测试课程数据"""
    courses_data = [
        {
            'title': 'Python基础编程',
            'subject': '计算机科学',
            'syllabus': '学习Python编程语言的基础知识，包括变量、函数、类等概念。掌握Python语法、数据类型、控制结构、函数定义、面向对象编程等核心概念。',
            'content': 'Python基础语法\n变量和数据类型\n控制结构(if/for/while)\n函数定义和调用\n类和对象\n模块和包\n异常处理\n文件操作'
        },
        {
            'title': '数据结构与算法',
            'subject': '计算机科学', 
            'syllabus': '学习常用的数据结构和算法，提高编程能力和解决问题的思维。包括数组、链表、栈、队列、树、图等数据结构，以及排序、搜索等经典算法。',
            'content': '数组和链表\n栈和队列\n树结构(二叉树、平衡树)\n图结构和图算法\n排序算法(冒泡、快排、归并)\n搜索算法(二分查找、DFS、BFS)\n动态规划\n贪心算法'
        },
        {
            'title': 'Web开发入门',
            'subject': '计算机科学',
            'syllabus': '学习HTML、CSS、JavaScript等前端技术，以及后端开发基础。掌握现代Web开发的核心技术栈。',
            'content': 'HTML结构和语义\nCSS样式和布局\nJavaScript基础\nDOM操作\n响应式设计\nAjax和API调用\n前端框架入门\n后端基础概念'
        }
    ]
    
    print("开始恢复课程数据...")
    created_count = 0
    
    for course_data in courses_data:
        course, created = Course.objects.get_or_create(
            title=course_data['title'],
            defaults=course_data
        )
        if created:
            created_count += 1
            print(f"✅ 创建课程: {course.title}")
        else:
            print(f"📋 课程已存在: {course.title}")
    
    total_courses = Course.objects.count()
    print(f"\n✅ 恢复完成！共有 {total_courses} 门课程，新创建 {created_count} 门课程。")

if __name__ == "__main__":
    restore_courses() 