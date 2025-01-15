from django.urls import path  # 用于定义路由
from .views import handle_image_request  # 导入视图

# 定义应用的路由
urlpatterns = [
    path('images/', handle_image_request, name='image_view'),
]