from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.hashers import make_password,check_password
from myadmin.models import Users
from myhome.models import Address


# 个人中心首页
def myhome_personal(request):
    return render(request,'myhome/Users/personal.html')

# 地址管理
def myhome_address(request):
    from django.core.paginator import Paginator
    type = request.session['VipUser']['uid']
    ob = Address.objects.filter(uid__contains=type)
    count = Address.objects.filter(uid__contains=type).count()
    context = {'ob':ob,'count':count}
    return render(request,'myhome/Users/address.html',context)

# 设为默认地址
def myhome_address_def(request):
    uid = request.GET.get('uid')
    print(uid)
    Address.objects.filter(uid=uid).update(status=1)
    # Address.objects.filter(id=vid).update(status=0)
    return HttpResponse('<script>alert("设置成功");location.href="/address/";</script>')

# 编辑收货地址页面
def myhome_address_edit(request):
    vid = request.GET.get('vid')
    context = {'vid':vid}
    return render(request,'myhome/Users/edit.html',context)

# 执行编辑操作
def myhome_address_doedit(request):
    vid = request.GET.get('vid')
    data = request.POST.dict()
    data.pop('csrfmiddlewaretoken')
    Address.objects.filter(id=vid).update(name=data['name'],address=data['address'],phone=data['phone'])
    return HttpResponse('<script>alert("编辑成功");location.href="/address/";</script>')

# 删除收货地址
def myhome_address_del(request):
    vid = request.GET.get('vid')
    Address.objects.filter(id=vid).delete()
    return HttpResponse('<script>alert("删除成功");location.href="/address/";</script>')