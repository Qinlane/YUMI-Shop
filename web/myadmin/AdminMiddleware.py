from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
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


        # 前台登陆验证
        homeurl=[
            reverse('myhome_personal'),
            reverse('myhome_information'),
            reverse('myhome_doinfor'),
            reverse('myhome_safety'),
            reverse('myhome_password'),
            reverse('myhome_passwordmol'),
            reverse('myhome_phone'),
            reverse('myhome_phone_change'),
            reverse('myhome_email'),
            reverse('myhome_email_bind'),
            reverse('myhome_collect'),
            reverse('myhome_collect_del'),
            reverse('myhome_address'),
            reverse('myhome_address_def'),
            reverse('myhome_address_add'),
            reverse('myhome_address_doadd'),
            reverse('myhome_address_edit'),
            reverse('myhome_address_doedit'),
            reverse('myhome_address_del'),
            reverse('myhome_email_html'),
            reverse('myhome_cart_index'),
            reverse('myhome_cart_add'),
            reverse('myhome_cart_del'),
            reverse('myhome_cart_clear'),
            reverse('myhome_cart_edit'),
            reverse('myhome_order_confirm'),
            reverse('myhome_order_create'),
            reverse('myhome_order_pay'),
        ]
        # 判断用户是否进入以上需要登陆的页面
        if path in homeurl:
            if not request.session.get('VipUser',None):
                # 如果没登陆则跳转
                return HttpResponse('<script>alert("请先登录!");location.href="/login/";</script>')

        response=self.get_response(request)
        return response
