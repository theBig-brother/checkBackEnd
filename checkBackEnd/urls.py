"""
URL configuration for checkBackEnd project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from image_upload.views import ImageUploadView
from . import views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('quickManage.urls')),
                  # path("", views.hello, name="hello"),
                  path('runoob/', views.runoob),
                  path('upload/', ImageUploadView.as_view(), name='image-upload'),
                  # path('management/',include('management_api.urls'), name='management'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 开发模式下服务媒体文件
