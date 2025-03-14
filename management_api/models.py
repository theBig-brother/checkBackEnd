import os

from django.db import models

# Create your models here.
from django.db import connection

from checkBackEnd import settings


def get_image_data(page,quantity):
    offset = (page - 1) * quantity
    with connection.cursor() as cursor:
        # 执行原生SQL查询
        # LIMIT关键字用于限制查询结果的数量。OFFSET 用于指定跳过多少行。它通常和 LIMIT 一起使用，帮助实现分页。
        cursor.execute('SELECT id, path FROM image_upload_image LIMIT %s OFFSET %s', [quantity, offset])
        # 获取所有查询结果
        rows = cursor.fetchall()
        # 执行查询获取数据表的总行数
        # COUNT(*)是一个聚合函数，用于返回指定表中记录的总数量。* 表示计算所有的行，包括表中的所有列，即使某些列值为 NULL，也会计入在内。如果你只想统计某一列的非 NULL 值数量，可以使用 COUNT(列名)，但在这种情况下，COUNT(*) 会统计所有行，无论列中是否包含 NULL。
        cursor.execute('SELECT COUNT(*) FROM image_upload_image')
        total_rows = cursor.fetchone()[0]  # 获取查询结果的第一列
    return rows,total_rows
    # for row in rows:
    #     print(f"ID: {row[0]}, Path: {row[1]}")
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

