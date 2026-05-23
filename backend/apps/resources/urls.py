# # backend/apps/resources/urls.py
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import CourseResourceViewSet, ResourceCollectionViewSet
#
# router = DefaultRouter()
# router.register(r'resources', CourseResourceViewSet, basename='resource')
# router.register(r'collections', ResourceCollectionViewSet, basename='collection')
#
# urlpatterns = [
#     path('', include(router.urls)),
#     path('by-course/', CourseResourceViewSet.as_view({'get': 'by_course'}), name='resources-by-course'),
#     path('export/', CourseResourceViewSet.as_view({'post': 'export'}), name='export-resources'),
# ]

from django.urls import path
from .views import CourseResourceViewSet, ResourceCollectionViewSet

urlpatterns = [
    path('', CourseResourceViewSet.as_view({'get': 'list', 'post': 'create'}), name='resource-list'),
    path('<int:pk>/', CourseResourceViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='resource-detail'),
    path('<int:pk>/download/', CourseResourceViewSet.as_view({'get': 'download'}), name='resource-download'),
    path('collections/', ResourceCollectionViewSet.as_view({'get': 'list', 'post': 'create'}), name='collection-list'),
]
