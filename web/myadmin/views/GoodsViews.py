from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.core.paginator import Paginator

from .CatesViews import get_cates_all
from .UsersViews import uploads_pic
from .. models import Cates, Goods

# Create your views here.


def goods_index(request):
    # 获取当前所有的商品数据
    data=Goods.objects.all()

      # 获取搜索条件
    types = request.GET.get('types',None)
    keywords = request.GET.get('keywords',None)
    # 判断是否搜索
    if types:
        from django.db.models import Q
        data = data.filter(Q(id__contains=keywords)|Q(goodsname__contains=keywords)|Q(title__contains=keywords))
    elif types:
        search = {types+'__contains':keywords}
        data = data.filter(**search)
    
    
    # 实例化分页类
    p = Paginator(data,10) 
    print(p.num_pages)
    # 获取当前的页码数
    pageindex=request.GET.get('page',1)

    # 获取当前页的数据
    goodslist=p.page(pageindex)

    # 分配数据
    context={'goodslist':goodslist}

    # 加载模板
    return render(request,'myadmin/goods/index.html',context)


def goods_insert(request):
    try:
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')
        # 处理 分类对象
        data['cateid'] = Cates.objects.get(id=data['cateid'])

        # 判断是否有图片上传
        myfile = request.FILES.get('pic', None)
        if not myfile:
            return HttpResponse('<script>alert("必须上传商品图片!");history.back(-1);</script>')
        data['pic_url'] = uploads_pic(myfile)

        # 执行添加
        ob = Goods(**data)
        ob.save()
        return HttpResponse('<script>alert("商品添加成功!");location.href="/myadmin/goods/index/";</script>')
    except:
        pass

    return HttpResponse('<script>alert("商品添加失败!");history.back(-1);</script>')


def goods_add(request):

     # 获取当前所有的分类数据
    data = get_cates_all(request)
    context = {'catelist': data}

    # 加载模板
    return render(request, 'myadmin/goods/add.html', context)

def goods_edit(request):
    # 接收用户id
    uid = request.GET.get('uid')
    # 获取当前用户的对象
    ob = Goods.objects.get(id=uid)

    print(ob.brand)
    # 判断当前的请求方式
    if request.method == 'POST':
        # 执行更新操作
        myfile = request.FILES.get('pic',None)
        if myfile:
            # 如果有新头像上传则先删除原头像
            os.remove(BASE_DIR+ob.pic_url)
            # 上传新头像
            ob.pic_url = uploads_pic(myfile)

        # 更新其他字段
        ob.goodsname = request.POST.get('goodsname')
        ob.title = request.POST.get('title')
        ob.price = request.POST.get('price')
        ob.brand = request.POST.get('brand')
        ob.color = request.POST.get('color')
        ob.size = request.POST.get('size')
        ob.goodsnum = request.POST.get('goodsnum')
        ob.goodsinfo = request.POST.get('goodsinfo')
        ob.save()
        return HttpResponse('<script>alert("更新成功");location.href="/myadmin/goods/index/";</script>')
    else:

        # 显示编辑表单
        context={'uinfo':ob}
        # 加载模板
        return render(request,'myadmin/goods/edit.html',context)

# 删除
def goods_del(request):
    # 接收数据
    cid = request.GET.get('cid')
    ordernum = request.GET.get('ordernum')

    # 获取当前用户的对象
    ob = Goods.objects.get(id=cid)
    if ob.ordernum>0:
        # 有订货
        return JsonResponse({'msg':'当前类下商品有订购，不能删除','code':1})

    # 判断当前分类下是否还有商品发布


    # 执行删除
    ob = Goods.objects.get(id=cid)
    ob.delete()
    return JsonResponse({'msg':'删除成功','code':0})