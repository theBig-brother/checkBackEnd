# myapp/urls.py
from django.urls import path
from . import views  # 导入视图文件

urlpatterns = [
    path('', views.hello, name='hello_view'),  # 路由到 views.some_view
    path('images', views.images, name='images_view'),  # 路由到 views.another_view
]
