from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.urls import reverse
from myadmin.models import Cates,Goods,Cart,Users,Order,OrderInfo
from myhome.models import Address


# 订单管理页面
def myhome_orderinfo(request):
    # 获取数据
    ob = Order.objects.filter(uid=request.session.get('VipUser')['uid'])
    print(ob)
    context = {'orderdata':ob}
    
    return render(request,'myhome/Users/orderinfo.html',context)