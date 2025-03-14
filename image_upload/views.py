# Create your views here.
# images/views.py
from io import BytesIO
from PIL import Image as PILImage
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Image
from .serializers import ImageSerializer
import piexif


# 未来如果不需要压缩，记得修改requirements.txt
def get_exif_data(image):
    """ 获取图片的 EXIF 信息 """
    exif_data = None
    try:
        if hasattr(image, '_getexif'):
            exif = image._getexif()
            if exif:
                # 提取所有 EXIF 标签
                exif_data = exif
    except AttributeError:
        pass
    return exif_data


class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        # 获取上传的文件
        file = request.data.get('file')

        if file is None:
            return Response({"detail": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)
        # 读取图片文件
        image = PILImage.open(file)
        image_file=  press(image,file.name,False)
        # print("type(image_file)",type(image_file),type(image))
        # 保存压缩后的文件到数据库
        img_instance = Image.objects.create(path=image_file)

        # 使用序列化器返回上传的图片信息
        serializer = ImageSerializer(img_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

def press(image,name,press=True):
    # 获取原始图片的 EXIF 数据
    exif_data = get_exif_data(image)
    exif_bytes =None
    if exif_data is not None:
    # 使用 piexif 来转换 EXIF 数据并将其嵌入到图像中
        exif_bytes = piexif.dump(exif_data)  # 将 EXIF 数据转换为字节流格式
        # print("exif_bytes")
        # piexif.dump(exif_bytes)

    # 设置图片质量和压缩尺寸
    max_quality = 85  # 设置 JPG 图片压缩的最大质量，质量越低文件越小
    max_width = 1200  # 可以设置最大宽度来压缩图片尺寸
    max_height = 1200  # 可以设置最大高度来压缩图片尺寸

    # 如果图片的宽度大于最大宽度，按比例调整
    if image.width > max_width or image.height > max_height:
        image.thumbnail((max_width, max_height))  # 调整图片大小，保持宽高比

    # 创建一个 BytesIO 对象用于保存压缩后的图片
    img_io = BytesIO()
    if press:
        if exif_bytes is not None:
            image.save(img_io, format='JPEG', quality=max_quality, exif=exif_bytes)
        else:
            image.save(img_io, format='JPEG', quality=max_quality)
    else:
        image.save(img_io, format='JPEG')
    img_io.seek(0)  # 将指针移动到文件开始

    # 创建一个 InMemoryUploadedFile 对象，用于替代原始文件
    image_file = InMemoryUploadedFile(
        img_io, None, name, 'image/jpeg', img_io.tell(), None
    )
    return image_file