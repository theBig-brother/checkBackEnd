# from django.db.models.functions import math
import json
import math

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from image_upload.models import Image
from .models import *
# Create your views here.

from django.templatetags.static import static


def index(request):
    menuitems = [
        {"key": "1", "icon": static('public/webstorm-icon-logo.svg'), "url": "/gallery/", "value": "图片管理"},
        {"key": "2", "icon": static('public/javascript.svg'), "url": "/dashboard/", "value": "仪表盘"},
        {"key": "3", "icon": static('public/typescript.svg'), "url": "/user/", "value": "用户"},
        {"key": "4", "icon": static('public/vite.svg'), "url": "/setting/", "value": "设置"},
        {"key": "5", "icon": static('public/vite.svg'), "url": "/test/", "value": "正在开发中……"},
    ]
    context = {"menuItems": menuitems,
               "defaultUrl": menuitems[0]["url"] if menuitems else "/default/"
               }

    return render(request, "index.html", context)


def dashboard(request):
    return render(request, "page/dashboard.html")


def test(request):
    return render(request, "page/test.html")


# 允许iframe跨域
@xframe_options_exempt
def user(request):
    return render(request, "page/user.html")


def setting(request):
    return render(request, "page/setting.html")


def gallery(request):
    if request.method == 'GET':
        howManyPerPage = 20
        lists = [{"Path": "https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png"}] * howManyPerPage
        # pages = 5
        pages = math.ceil(howManyPages() / howManyPerPage)
        images = get_image_data(pages, howManyPerPage)
        print(images)
        current_page = int(request.GET.get('page', 1))  # Get the page from the query params or default to 1
        return render(request, "page/gallery.html",
                      {"lists": images, "pages": pages, 'current_page': current_page})


@csrf_exempt  # 取消 CSRF 验证
def del_image(request):
    if request.method == 'GET':
        return HttpResponse("你干嘛对一个del方法发送GET请求")
    if request.method == 'DELETE':
        try:
            body = json.loads(request.body)
            item_id = body.get('id')
            item = Image.objects.get(pk=item_id)
            print(item.path)

            # 获取 Item 实例
            image = Image.objects.get(pk=item_id)

            # 获取文件路径
            file_path = item.path.path

            # 检查文件是否存在
            if os.path.exists(file_path):
                os.remove(file_path)  # 删除文件
            else:
                return JsonResponse({'error': 'File not found'}, status=404)

            image.delete()
            return JsonResponse({'status': 'deleted'})
        except Image.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=404)
    return JsonResponse({'error': 'Invalid method'}, status=400)
