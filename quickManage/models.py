from django.db import models

# Create your models here.
from django.db import connection

from checkBackEnd import settings
import os


def howManyPages():
    with connection.cursor() as cursor:
        cursor.execute('SELECT COUNT(*) FROM image_upload_image')
        total_rows = cursor.fetchone()[0]  # 获取查询结果的第一列
    return total_rows


def get_image_data(page,quantity):
    offset = (page - 1) * quantity
    with connection.cursor() as cursor:
        # 执行原生SQL查询
        # LIMIT关键字用于限制查询结果的数量。OFFSET 用于指定跳过多少行。它通常和 LIMIT 一起使用，帮助实现分页。
        cursor.execute('SELECT id, path FROM image_upload_image LIMIT %s OFFSET %s', [quantity, offset])
        # 获取所有查询结果
        rows = cursor.fetchall()
    result=[]
    for row in rows:
        result.append({"ID": row[0], "Path":"http://127.0.0.1:8000/media/"+ row[1]})
    return result
def del_image_data(imageId):
    with connection.cursor() as cursor:
        # 执行原生SQL查询
        cursor.execute("SELECT path FROM image_upload_image WHERE id = %s", (imageId,))
        # 获取所有查询结果
        result = cursor.fetchall()
        # 如果找到了对应的图片
        if result:
            print("deleting image")
            image_path = settings.MEDIA_ROOT+"/"+result[0][0]
            print("image_path",image_path)
            # 删除文件
            if os.path.exists(image_path):
                os.remove(image_path)

            # 删除数据库中对应的记录
            cursor.execute("DELETE FROM image_upload_image WHERE id = %s", (imageId,))
            connection.commit()
            return f"Image with ID {imageId} and path {image_path} has been deleted successfully."
        else:
            return f"No image found with ID {imageId}."

