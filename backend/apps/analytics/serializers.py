from rest_framework import serializers
from .models import LearningAnalytics

class LearningAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningAnalytics
        fields = '__all__'
        read_only_fields = ['last_updated']
