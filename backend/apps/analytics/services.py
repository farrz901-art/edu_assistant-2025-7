from .models import LearningAnalytics


class AnalyticsService:
    def update_analytics(self, user, course_id, result):
        analytics, created = LearningAnalytics.objects.get_or_create(
            student=user,
            course_id=course_id,
            defaults={
                'completion_rate': 0,
                'accuracy_rate': 0,
                'weak_topics': []
            }
        )

        # 更新分析数据
        analytics.update_analytics(result)
