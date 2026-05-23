"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.conf.urls.static import static

# API的根视图，可以展示API的概览或欢迎信息
def api_root_view(request):
    return JsonResponse({'message': '教学实训智能体平台 API'}, status=200)

# 定义所有API子路由
api_urlpatterns = [
    path('', api_root_view), # /api/
    path('courses/', include('apps.courses.urls')),
    path('ai/', include('apps.ai_services.urls')),
    path('analytics/', include('apps.analytics.urls')),
    path('resources/', include('apps.resources.urls')),
    path('admin/', include('apps.admin.urls')),
]

# 主路由配置
urlpatterns = [
    # 将所有API路由统一包含在 /api/ 命名空间下
    path('api/', include(api_urlpatterns)),

    # 健康检查路径
    path('health/', lambda r: HttpResponse(status=200), name='health-check'),

    # 其他非API路径，例如重定向到前端
    path('', RedirectView.as_view(url='/', permanent=False)),
]

# 在开发模式下，添加媒体文件路由
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)













# from django.http import HttpResponse
# # from django.contrib import admin
# from django.urls import path
# from django.contrib import admin
# from django.urls import path, include
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from django.conf import settings
# from django.conf.urls.static import static
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#
#     # 应用路由
#     path('api/auth/', include('apps.users.urls')),
#     path('api/courses/', include('apps.courses.urls')),
#     path('api/ai/', include('apps.ai_services.urls')),
#     path('api/analytics/', include('apps.analytics.urls')),
#     path('api/resources/', include('apps.resources.urls')),
#     path('api/admin/', include('apps.admin.urls')),
#
#     # 健康检查
#     path('health/', lambda r: HttpResponse(status=200)),
# ]
#
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
