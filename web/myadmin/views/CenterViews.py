from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .. models import Cates,Goods,Cart,Users,Order,OrderInfo
from django.urls import reverse
# 导入分页类
from django.core.paginator import Paginator
from django.contrib.auth.decorators import permission_required

# Create your views here.

# 订单管理列表
@permission_required('myadmin_show_Order',raise_exception=True)
def center_index(request):
    # 获取数据
    data = Order.objects.all()
    # 获取搜索条件
    types = request.GET.get('types',None)
    keywords = request.GET.get('keywords',None)
    # 判断是否搜索
    if types:
        from django.db.models import Q
        data = data.filter(Q(id__contains=keywords)|Q(username__contains=keywords)|Q(phone__contains=keywords)
        |Q(address__contains=keywords)|Q(addtime__contains=keywords))
    elif types:
        search = {types+'__contains':keywords}
        data = data.filter(**search)

    # 实例化分页类
    p = Paginator(data,10) 
    # 获取当前的页码数
    pageindex=request.GET.get('page',1)

    # 获取当前页的数据
    cardata=p.page(pageindex)

    context={'cardata':cardata}

    return render(request,'myadmin/center/index.html',context)

# 订单修改
@permission_required('myadmin_create_Order',raise_exception=True)
def center_edit(request):

    # 接收用户id
    uid = request.GET.get('uid')
    # 获取当前用户的对象
    ob = Order.objects.get(id=uid)

    # 判断当前的请求方式
    if request.method == 'POST':
        # 执行更新操作           
        # 更新其他字段
        ob.username = request.POST.get('username')
        ob.phone = request.POST.get('phone')
        ob.address = request.POST.get('address')
        ob.totalprice = request.POST.get('totalprice')
        ob.status = request.POST.get('status')
        ob.paytype = request.POST.get('paytype')
        ob.addtime = request.POST.get('addtime')
        ob.paytime = request.POST.get('paytime')
        ob.save()
        return HttpResponse('<script>alert("更新成功");location.href="/myadmin/center/index/";</script>')
    else:
         # 显示编辑表单
        context={'uinfo':ob}
        # 加载模板
        return render(request,'myadmin/center/edit.html',context)

