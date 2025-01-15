"""
URL configuration for quickBackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('testapi/', include("testapi.urls")),  # 连接到 testapi 应用的路由
    # 包含 image_manager 应用的路由
    path('api/', include('image_manager.urls')),
]
# 如果是开发模式，确保 Django 处理静态文件和媒体文件
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# 配置媒体文件的访问路径（用于访问上传的图片）
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)