from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.urls import reverse
from myadmin.models import Cates,Goods,Cart,Users,Order,OrderInfo
from myhome.models import Address

# Create your views here.



# 确认订单
def myhome_order_confirm(request):
    # 获取选择的购物车 id
    cartidstr = request.GET.get('cartids')
    cartids = cartidstr.split(',')

    # 获取用户收货地址

    # 把当前选择的购物车数据查询处理
    data = Cart.objects.filter(id__in=cartids)
    address = Address.objects.filter(uid=request.session.get('VipUser')['uid'])
    # 分配数据
    context = {'cardata':data,'address':address}

    return render(request,'myhome/order/order.html',context)

def myhome_order_create(request):
    # 接收数据
    data = request.GET.dict()
    
     # 创建订单
    ob =  Order()
    ob.uid = Users.objects.get(id=request.session.get('VipUser')['uid'])
    ob.username = data['name']
    ob.phone = data['phone']
    ob.address = data['address']
    ob.totalprice = 0
    ob.save()
    print(data)

    # 创建订单详情
    cartdata = Cart.objects.filter(id__in = data['cartids'].split(','))
    totalprice = 0
    for x in cartdata:
        obinfo = OrderInfo()
        obinfo.orderid = ob
        obinfo.goodsid = x.goodsid
        obinfo.num = x.num
        obinfo.save()
        # 计算总价
        totalprice += x.num*x.goodsid.price
        # 删除购物车中已下单的商品
        x.delete()


    # 修改订单总价
    ob.totalprice = totalprice
    ob.save()
    did=str(ob.id)

    return JsonResponse({'code':0,'msg':'订单创建成功,请支付','oid':did})
    # <script>alert("订单创建成功,请支付");location.href="/order/pay/?orderid='+str(ob.id)+'"</script>

# 订单支付
def myhome_order_pay(request):
    orderid = request.GET.dict()

    return HttpResponse('123')

