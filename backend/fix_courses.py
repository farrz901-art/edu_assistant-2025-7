import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.courses.models import Course

def fix_course_data():
    """
    Finds all courses and updates them with a non-empty title and syllabus
    if they are currently empty.
    """
    courses_to_update = [c for c in Course.objects.all() if not c.title or not c.syllabus]
    
    if not courses_to_update:
        print("All courses already have a title and syllabus. No update needed.")
        return

    print(f"Found {len(courses_to_update)} courses to update...")

    for course in courses_to_update:
        course.title = f"课程 {course.id}"
        course.syllabus = f"这是课程 {course.id} 的教学大纲。"
        course.save()

    print(f"Successfully updated {len(courses_to_update)} courses.")

if __name__ == "__main__":
    fix_course_data() 