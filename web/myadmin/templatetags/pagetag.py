from django import template
register = template.Library()
from django.utils.html import format_html
from django.urls import reverse
from myadmin.models import Cates


# 自定义乘法运算标签
@register.simple_tag
def Product(var1,var2):
    res = float(var1) * float(var2)

    return '%.2f'%res


@register.simple_tag
def ShowsPage(count,request):
    # count  总页数
    # request  请求对象

    # 接受当前的页码数
    p= int(request.GET.get('page',1))
    print(count)
    # 获取当前请求的所有参数
    data = request.GET.dict()
    args=''
    print(data)
    # {'keywords': '147', 'types': 'phone'}
    # {'page': '2'}
    for k,v in data.items():
        print(k,v)
        if k != 'page':
            args += '&'+k+'='+v

    start = p-5
    end = p+4
    # 判断如果当前页 小于5
    if p<=5:
        start=1
        end=10
    # 判断如果当前页大于总页数-5
    if p>count-5:
        start=count-9
        end=count
    # 判断如果总页数 小于10
    if count<10:
        start=1
        end=count

    pagehtml = ''
    # 首页
    pagehtml+='<li ><a class="btn btn-info"href="?page=1{args}">首页</a></li>'.format(args=args)
    # 上一页
    if p>1:
        pagehtml+='<li ><a class="btn btn-info"href="?page={p}{args}">上一页</a></li>'.format(p=p-1,args=args)

    for x in range(start,end+1):
        # 判断当前页
        if p == x:
            pagehtml+= '<li><a  class="btn btn-info active"href="?page={p}{args}">{p}</a></li>'.format(p=x,args=args)
        else:
            pagehtml+='<li ><a class="btn btn-info"href="?page={p}{args}">{p}</a></li>'.format(p=x,args=args)
    # 下一页
    if p<count:
        pagehtml+='<li ><a class="btn btn-info"href="?page={p}{args}">下一页</a></li>'.format(p=p+1,args=args)
    
    # 尾页
    pagehtml+='<li><a  class="btn btn-info"href="?page={p}{args}">尾页</a></li>'.format(p=count,args=args)

    return format_html(pagehtml)

@register.simple_tag
def ShowNav():
    # 获取一级分类
    CatesList = Cates.objects.filter(pid=0)
    # 分配数据

    s=''
    for x in CatesList:
       s+='''
       <li><a href="{url}" target="_blank">{name}</a></li>
       '''.format(name=x.name,url=reverse('myhome_list',args=(x.id,)))


    return format_html(s)


