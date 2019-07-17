from django.shortcuts import render
from django.http import HttpResponse
import re


class AdminLoginMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
        # One-time configuration and initialization.

    def __call__(self,request):
        # 用户的请求路径
        path=request.path
        # 定义允许访问的路径
        urllist= ['/myadmin/login/','/myadmin/dologin/','/myadmin/verifycode/']
        # 检测当前的请求是否已经登录了，如果已经登录则放行，如果未登录则跳转登录页
        if re.match('/myadmin/',path) and path not in urllist:
            # 检测是否已登录
            AdminUser=request.session.get('AdminUser',None)
            if not AdminUser:

                return HttpResponse('<script>alert("请先登录!");location.href="/myadmin/login/";</script>')
       
        response=self.get_response(request)
        return response
