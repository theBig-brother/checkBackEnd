import json
import os

from django.http import FileResponse, Http404, JsonResponse,HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from checkBackEnd import settings
from .models import *
# Create your views here.
def hello(request):
    rows=get_image_data(0,20)
    return HttpResponse(rows[0][1])
    # return render(request, 'hello.html')

@csrf_exempt  # 取消 CSRF 验证
def images(request):
    SM=settings.MEDIA_URL
    SMR=settings.MEDIA_ROOT
    if request.method == 'GET':
        image_urls=[]
        page = request.GET.get('page', '')
        quantity=request.GET.get('quantity', '')
        page=int(page)
        quantity=int(quantity)
        rows,image_length = get_image_data(page,quantity)
        for row in rows:
            image_urls.append([row[0],SM+row[1]])

        # image_path = os.path.join(settings.MEDIA_ROOT, filename)  # 拼接图片路径
        # if not os.path.exists(image_path):
        #     raise Http404("Image not found")  # 图片不存在返回 404
        #
        # return FileResponse(open(image_path, 'rb'), content_type='image/jpeg')  # 以流方式返回图片

        return JsonResponse({'imageInfo': image_urls,"totalImages":image_length})
        # return HttpResponse(param)
    elif request.method == 'POST':
        data = json.loads(request.body)
        param = data.get('param', '')
        print(param)
        return HttpResponse("This is a POST request")
    elif request.method == 'DELETE':
        print("DELETE")
        data = json.loads(request.body)
        imageId = data.get('imageId', '')
        del_image_data(imageId)
        # print("param",param.split(SM))
        return HttpResponse("This is a DELETE request")
    else:
        return HttpResponse("Other request method")