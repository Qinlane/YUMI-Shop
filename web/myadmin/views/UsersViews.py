from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import os
from django.contrib.auth.hashers import make_password, check_password
# 导入分页类
from django.core.paginator import Paginator
from ..models import Users
from web.settings import BASE_DIR
from django.contrib.auth.decorators import permission_required



# Create your views here.
# 用户模型的管理
# 会员添加表单
@permission_required('myadmin.create_User',raise_exception=True)
def user_add(request):

    return render(request,'myadmin/users/add.html')

# 会员执行添加
@permission_required('myadmin.create_User',raise_exception=True)
def user_insert(request):
    # 接收表单数据
    data=request.POST.dict()
    data.pop('csrfmiddlewaretoken')

    # 处理密码 加密
    data['password'] = make_password(data['password'],None, 'pbkdf2_sha256')

    # 头像上传
    # 接收上传的文件
    myfile = request.FILES.get('pic',None)
    if not myfile:
        # 没有上传头像
        return HttpResponse('<script>alert("没有选择头像上传");history.back(-1);</script>')
    # 处理头像上传  1.jpg ==> [1,jpg]
    data['pic_url']=uploads_pic(myfile)

    try:
        # 创建模型，添加数据
        ob = Users(**data)
        ob.save()
        return HttpResponse('<script>alert("添加成功");location.href="/myadmin/user/index";</script>')
    except:
        pass
    return HttpResponse('<script>alert("添加失败");history.back(-1);</script>')

    
# 会员列表
@permission_required('myadmin.show_User',raise_exception=True)
def user_index(request):
    # 获取所有用户的数据
    data = Users.objects.all()

    # 获取搜索条件
    types = request.GET.get('types',None)
    keywords = request.GET.get('keywords',None)
    # 判断是否搜索
    if types:
        from django.db.models import Q
        data = data.filter(Q(id__contains=keywords)|Q(nikename__contains=keywords)|Q(phone__contains=keywords)|Q(email__contains=keywords))
    elif types:
        search = {types+'__contains':keywords}
        data = data.filter(**search)
    
    print(data)
    # 实例化分页类
    p = Paginator(data,10) 

    # 获取当前的页码数
    pageindex=request.GET.get('page',1)

    # 获取当前页的数据
    userlist=p.page(pageindex)

    # 分配数据
    context={'userlist':userlist}

    # 加载模板
    return render(request,'myadmin/users/index.html',context)

# 会员编辑
@permission_required('myadmin.edit_User',raise_exception=True)
def user_edit(request):
    # 接收用户ID
    uid = request.GET.get('uid')
    # 获取当前会员对象
    ob = Users.objects.get( id=uid)

    # 判断当前的请求方式
    if request.method=='POST':
        # 执行更新
        # 判断密码是否更新
        password_now=request.POST.get('password',None)
        if password_now:
            # 更新密码
            ob.password=make_password(request.POST['password'],None,'pbkdf2_sha256')
        
        myfile = request.FILES.get('pic',None)
        myfile_now = request.POST.get('pic_url',None)

        # 判断数据库中的pic_url是否为空
        if myfile_now:
            if myfile:
                # 如有新头像上传，则先删除原头像
                os.remove(BASE_DIR+ob.pic_url)
                ob.pic_url=uploads_pic(myfile)
        else:
            ob.pic_url=uploads_pic(myfile)


        # 更新其他字段
        ob.nikename = request.POST.get('nikename')
        ob.email = request.POST.get('email')
        ob.phone = request.POST.get('phone')
        ob.age = request.POST.get('age')
        ob.sex = request.POST.get('sex')
        ob.save()
        return HttpResponse('<script>alert("更新成功");location.href="/myadmin/user/index/";</script>')
    else:

        # 显示编辑表单
        context={'uinfo':ob}
        # 加载模板
        return render(request,'myadmin/users/edit.html',context)

# 会员状态更新
def user_set_status(request):
    # 通过uid获取当前会员对象
    ob=Users.objects.get(id=request.GET.get('uid'))
    ob.status = request.GET.get('status')
    ob.save()
    return JsonResponse({'msg':'状态更新成功','code':0})


# 处理头像上传代码 
def uploads_pic(myfile):
    try:
        import time
        filename = str(time.time())+"."+myfile.name.split('.').pop()
        destination = open(BASE_DIR+"/static/uploads/"+filename,"wb+")
        for chunk in myfile.chunks():      # 分块写入文件  
            destination.write(chunk)  
        destination.close()
        return '/static/uploads/'+filename
    except:
        return False

