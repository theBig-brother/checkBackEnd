from django.shortcuts import render
import logging
# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


# 获取日志记录器
logger = logging.getLogger('myapp')

@api_view(['GET',"POST"])
def goods_list(request):
    goods1={"name":"ceshi1","price":12}
    logger.info("ok"+str(request))
    return Response(goods1,status=status.HTTP_200_OK)
