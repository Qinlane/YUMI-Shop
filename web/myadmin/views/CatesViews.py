from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .. models import Cates
from django.urls import reverse
# 导入分页类
from django.core.paginator import Paginator
from django.contrib.auth.decorators import permission_required

# Create your views here.


def get_cates_all(request):
    
    # select *,concat(path,id) as paths from myadmin_cates order by paths;
      # 获取所有分类
    data= Cates.objects.extra(select ={'paths':'concat(path,id)'}).order_by('paths')
     # 获取搜索条件
    types = request.GET.get('types',None)
    keywords = request.GET.get('keywords',None)
    # 判断是否搜索
    if types:
        from django.db.models import Q
        data = data.filter(Q(id__contains=keywords)|Q(name__contains=keywords))
    elif types:
        search = {types+'__contains':keywords}
        data = data.filter(**search)

    for x in data:
        l=x.path.count(',')-1
        
        x.sub=l*'>'
        if x.pid==0:
            x.pname='顶级分类'
        else:
            pob = Cates.objects.get(id=x.pid)
            x.pname = pob.name

    return data

# 分类列表
@permission_required('myadmin.show_Cates',raise_exception=True)
def cate_list(request):
    data=get_cates_all(request)
    # data = Cates.objects.all()

     # 实例化分页类
    p = Paginator(data,10) 
    print(data)
    # 获取当前的页码数
    pageindex=request.GET.get('page',1)

    # 获取当前页的数据
    catelist=p.page(pageindex)
    # 分配数据
    context = {'catelist':catelist}
    # 加载模板
    return render(request,'myadmin/cates/index.html',context)

# 分类添加
@permission_required('myadmin.create_Cates',raise_exception=True)
def cate_add(request):
    if request.method == 'POST':
        # 接收数据
        data={}
        data['name'] = request.POST.get('name')
        data['pid']=request.POST.get('pid')
        # data['path']='0,'

        # 判断path路径
        if data['pid'] == '0':
            data['path'] = '0,'
        else:
            # 获取当前父级的path路径
            pob = Cates.objects.get(id=data['pid'])
            # 拼接当前数据的path
            data['path'] = pob.path+data['pid']+','
        print(data,data['pid'])
        # 数据入库
        ob = Cates(**data)
        ob.save()

        return HttpResponse('<script>alert("添加成功");location.href="'+reverse('myadmin_cate_add')+'";</script>')
    else:
        # 获取当前已有的 分类
        catelist=get_cates_all(request)
        # # 分配数据
        context = {'catelist':catelist}
        # # 加载模板

        return render(request,'myadmin/cates/add.html',context)

# 分类删除
def cate_del(request):
    # 接收数据
    cid = request.GET.get('cid')

    # 判断当前分类下是否还有子类
    res = Cates.objects.filter(pid=cid).count()
    if res:
        # 有子类
        return JsonResponse({'msg':'当前类下有子类，不能删除','code':1})

    # 判断当前分类下是否还有商品发布


    # 执行删除
    ob = Cates.objects.get(id=cid)
    ob.delete()
    return JsonResponse({'msg':'删除成功','code':0})
    

# 分类名称修改
def cate_edit(request):
    try:
        # 获取 参数
        cid=request.GET.get('cid')
        newname=request.GET.get('newname')

        # 获取对象
        ob = Cates.objects.get(id=cid)
        ob.name=newname
        # 保存修改
        ob.save()
        data={'msg':'更新成功','code':0}
    except:
        data={'msg':'更新失败','code':1}

    return JsonResponse(data)
