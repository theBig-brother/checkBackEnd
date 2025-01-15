import json

from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import HttpRequest
from quickBackend import settings
from .models import Image
from django.db import IntegrityError
import logging

# 获取日志记录器
logger = logging.getLogger('myapp')

@csrf_exempt
@api_view(['GET','POST','DELETE'])
def handle_image_request(request):
    if request.method == 'POST':
        # 处理图片上传
        if not request.content_type.startswith('multipart/form-data'):
            return JsonResponse({'error': 'Content-Type 必须是 multipart/form-data'}, status=400)
        # 打印 request.FILES 的所有键值对

        image_files = request.FILES.getlist('image')
        if not image_files:
            return JsonResponse({'error': '没有提供图片文件'}, status=400)

        # 保存图片文件
        image_instances = [Image.objects.create(image=image) for image in image_files]
        return JsonResponse({'message': '图片上传成功', 'ids': [image.id for image in image_instances]}, status=201)

    elif request.method == 'GET':

        # 获取分页参数

        try:
            page = int(request.GET.get('page', 1))  # 从查询参数中获取分页信息
        except ValueError:
            return JsonResponse({'error': '分页参数无效'}, status=400)
        images = Image.objects.all().order_by('uploaded_at')
        paginator = Paginator(images, 20)
        try:
            page_obj = paginator.page(page)
        except Exception:
            return JsonResponse({'error': '页码无效或不存在'}, status=404)
        # 构建图片 URL 列表
        image_urls = [request.build_absolute_uri(image.image.url) for image in page_obj]
        return JsonResponse({
            'images': image_urls,
            'total_images': paginator.count,
            'total_pages': paginator.num_pages,
        }, status=200)
    elif request.method == 'DELETE':
        try:
            # 获取请求数据
            data = json.loads(request.body.decode('utf-8'))  # 将请求体解析为 JSON 对象
            image_url = data.get("imageUrl")  # 获取图片的 URL

            if not image_url:
                return JsonResponse({"error": "缺少图片 URL"}, status=400)

            # 根据存储路径来查找图片实例，假设 URL 中的路径去掉了 'MEDIA_URL' 部分
            # 比如图片 URL 是 'http://example.com/media/images/photo1.jpg'
            base_url = f"{request.scheme}://{request.get_host()}"
            image_path = image_url.replace(base_url+settings.MEDIA_URL, '')  # 移除 MEDIA_URL 部分

            # image_instance = Image.objects.filter(image__exact=image_url).first()
            image_instance = Image.objects.filter(image__exact=image_path).first()

            if not image_instance:
                logger.error(f'发生错误: {str(image_instance),str(image_path),str(image_url)}', exc_info=True)  # 记录错误及堆栈信息
                return JsonResponse({"error": "图片未找到"}, status=404)

            # 删除图片实例
            image_instance.delete()

            return JsonResponse({"message": "图片删除成功"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({'error': '不支持的 HTTP 方法'}, status=405)
       # logger.error(f'发生错误: {str(e)}', exc_info=True)  # 记录错误及堆栈信息