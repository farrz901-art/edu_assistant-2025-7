from django.urls import path
from .views import (
    AskQuestionAPIView,
    AnswerEvaluationAPIView, 
    PracticeGeneratorAPIView,
    CourseDesignAPIView,
    AssessmentGeneratorAPIView,
    LearningDataAnalysisAPIView
)

urlpatterns = [
    path('ask/', AskQuestionAPIView.as_view(), name='ask-question'),
    path('evaluate/', AnswerEvaluationAPIView.as_view(), name='evaluate-answer'),
    path('practice/', PracticeGeneratorAPIView.as_view(), name='generate-practice'),
    path('design_course/', CourseDesignAPIView.as_view(), name='design-course'),
    path('generate_assessment/', AssessmentGeneratorAPIView.as_view(), name='generate-assessment'),
    path('analyze_learning_data/', LearningDataAnalysisAPIView.as_view(), name='analyze-learning-data'),
]
