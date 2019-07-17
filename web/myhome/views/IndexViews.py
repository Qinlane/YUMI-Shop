from django.shortcuts import render
from django.http import HttpResponse, Http404

from myadmin.models import Cates,Goods
# Create your views here.

# 首页
def myhome_index(request):

    # 先获取一级分类
    data = Cates.objects.filter(pid=0)
    # 在一级分类下  追加一个sub属性
    for x in data:
        # sub 属性里存放的是当前一级分类下的 二级子类
        x.sub = Cates.objects.filter(pid=x.id)
        # oub 属性里存放的是三级子类
        for c in x.sub:
            c.oub = Cates.objects.filter(pid=c.id)
        
    context = {'navdata':data}

    return render(request,'myhome/index.html',context)

# 获取第三级分类
def all_class():
    data = Cates.objects.filter(pid=0)
    for x in data:
        x.ssb = Cates.objects.filter(pid=x.id)
        # oub 属性里存放的是三级子类
        for c in x.ssb:
            c.oub = Cates.objects.filter(pid=c.id)
            for d in c.oub:
                d.dub = Cates.objects.filter(pid=d.id)
    
    return data
# 全部列表
def myhome_all_list(request):

    data = all_class()
    context = {'alllist':data}
    return render(request,'myhome/index/all_list.html',context)

# 列表
def myhome_list(request,cid):
    data = all_class()
      # 根据cid获取当前分类对象
    ob = Cates.objects.get(id=cid)
    # 判断当前是否为一级类
    if ob.pid > 0:
        # 获取当前一级类的所有子类
        ob.sub = Cates.objects.filter(pid=ob.id)
        # 获取当前二级分类下的所有商品
        goods = []
        for x in ob.sub:
            goods += x.goods_set.all().values()
        # 把当前分类下商品追加到数据中
        ob.goods = goods
        # 分配数据
        context = {'Cateslist':ob,'alllist':data}
    else:
        # 获取当前分类的 父级
        pob = Cates.objects.get(id=cid)
        # pob = Cates.objects.get(id=ob.pid)
        # 获取当前二级分类的 同级分类
        pob.sub = Cates.objects.filter(pid=pob.id)
        goods = []
        for x in pob.sub:
            x.ssb = Cates.objects.filter(pid=x.id)
            for c in x.ssb:
                c.oub = Cates.objects.filter(pid=c.id)
                goods += c.goods_set.all().values()
                if c.id == ob.id:
                    # 给当前的二级类加一个标识
                    x.index = True
        pob.goods = goods
        # 获取当前类下商品,不要同类的商品
        # pob.goods = ob.goods_set.all()
        # # 分配数据
        context = {'Cateslist':pob,'alllist':data}
    return render(request,'myhome/index/list.html',context)

# 详情
def myhome_info(request):
    # 根据商品id获取商品数据
    try:
        ob = Goods.objects.get(id = request.GET.get('goodsid'))
        ob.sizes = ob.sizes.strip(',').split(',')
        ob.color = ob.color.strip(',').split(',')
        # 通过id拿到cateid_id
        cid=ob.cateid_id
        # 获取当前分类的 父级
        pob = Cates.objects.get(id=cid)

        # 通过id拿到cateid_id
        pid = pob.pid
        # 获取当前分类的 父级 的 父级
        ppb = Cates.objects.get(id=pid)
        parent_stage=[]
        # 分配数据
        context = {'goods':ob,'Cateslist':pob,'Catesname':ppb}
        return render(request,'myhome/index/info.html',context)
    except:
        pass
    raise Http404('你需要的页面找不到路。。')
