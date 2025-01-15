import os
import shutil

import django
from django.conf import settings
from django.db import models

import image_manager

# 设置 Django 配置文件路径（确保用你的项目名替换 "myproject"）
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quickBackend.settings")

# 加载 Django 设置
django.setup()
# 假设你的Image模型是这样的

# class Image(models.Model):
#     image = models.ImageField(upload_to='images/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)
  # 导入图片模型
from image_manager.models import Image


# 提取并保存图片的函数
def save_images_from_db(db_path, output_folder):
    # 创建输出文件夹，如果文件夹不存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 连接到数据库并查询所有图片的路径
    from django.core.management import execute_from_command_line
    import sys
    sys.argv = ['manage.py', 'makemigrations']
    execute_from_command_line(sys.argv)


    # 查询所有图片
    images = Image.objects.all()

    # 遍历查询结果并复制图片
    for image in images:
        # 获取图片的路径
        image_path = image.image.path

        # 确保图片文件存在
        if os.path.exists(image_path):
            # 生成目标文件的路径（使用图片的文件名）
            output_image_path = os.path.join(output_folder, os.path.basename(image_path))

            # 将图片复制到输出文件夹
            shutil.copy(image_path, output_image_path)
            print(f"Image {image.id} copied to {output_image_path}")
        else:
            print(f"Image {image.id} not found at {image_path}")


# 调用函数
db_file_path = 'db.sqlite3'  # 替换为你的SQLite数据库路径
output_directory = 'output_images'  # 替换为你希望保存图片的文件夹路径

save_images_from_db(db_file_path, output_directory)
