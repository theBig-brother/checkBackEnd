from django.db import models

# Create your models here.
# images/models.py

class Image(models.Model):
    # 图片文件字段
    path = models.ImageField(upload_to='images/%Y/%m/%d/',
                             default='default.jpg')
    # 图片的上传时间
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} - {self.uploaded_at}"
