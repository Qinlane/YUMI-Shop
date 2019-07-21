from django.shortcuts import render
from django.http import HttpResponse, Http404,JsonResponse

from myadmin.models import Users,Cates,Goods,Cart

# 购物车列表
def myhome_cart_index(request):
    # 获取当前用户的购物车数据
    VipUser = request.session.get('VipUser')
    data = Cart.objects.filter(uid=VipUser['uid'])
    context = {'cartdata':data}

    return render(request,'myhome/cart/index.html',context)

def myhome_cart_add(request):
    
    try:
        # 执行购物车的商品添加
        data = request.GET.dict()
        data['goodsid'] = Goods.objects.get(id=data['goodsid'])
        data['uid'] = Users.objects.get(id=request.session.get('VipUser')['uid'])
        # 先检测当前的商品是否已经在当前用户的购物车中
        ob = Cart.objects.filter(uid=data['uid']).filter(goodsid=data['goodsid'])

        if ob.count():
            # 存在 获取当前购物车对象
            cart = Cart.objects.get(id=ob[0].id)
            num=int(data['num'])
            cart.num += num
            lengths=int(data['lengths'])
            if lengths==3:
                cart.sizes+=((','+data['sizes'])*num)
                cart.color+=((','+data['color'])*num)
                cart.save()
            elif lengths==2:
                cart.sizes=data['sizes']
                cart.color+=((','+data['color'])*num)
                cart.save()
            elif lengths==1:
                cart.sizes+=((','+data['sizes'])*num)
                cart.color=data['color']
                cart.save()
            else:
                cart.sizes=data['sizes']
                cart.color=data['color']
                cart.save()

        else:
            # 不存在
            # 存入 cart模型中
            ob = Cart(**data)
            num=int(data['num'])
            ob.num = num
            lengths=int(data['lengths'])

            ob.sizes=data['sizes']
            ob.color=data['color']
            ob.save()

        return JsonResponse({'code':0,'msg':'加入购物车成功!'})
    except:
        pass

    return JsonResponse({'code':1,'msg':'加入购物车失败!'})

# 商品删除
def myhome_cart_del(request):
    try:
        # cartid
        cartid = request.GET.get('cartid')
        # 获取当前购物车商品对象
        ob = Cart.objects.get(id=cartid)
        # 执行删除
        ob.delete()
        return JsonResponse({'code':0,'msg':'删除成功'})
    except:
        pass

    return JsonResponse({'code':1,'msg':'删除失败'})

# 购物车商品数量修改
def myhome_cart_edit(request):
    try:
        cartid = request.GET.get('cartid')
        num = request.GET.get('num')
        ob = Cart.objects.get(id=cartid)
        ob.num=num
        ob.save()

        return JsonResponse({'code':0,'msg':'删除成功'})
    except:
        pass

    return JsonResponse({'code':1,'msg':'删除失败'})

# 购物车空页
def myhome_cart_empty(request):
    

    return render(request,'myhome/cart/empty.html')

# 商品清空
def myhome_cart_clear(request):
    

    return HttpResponse('myhome_cart_clear')
