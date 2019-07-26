from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import Users
from django.core.paginator import Paginator
from django.contrib.auth.models import User,Permission,Group
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.hashers import make_password, check_password



# Create your views here.
def index(request):
    
    return render(request,'myadmin/index.html')

# 权限管理 管理员列表
@permission_required('auth.add_group',raise_exception=True)
def myadmin_authuser_index(request):
    # 获取当前已经创建的所有 组
    data = User.objects.all()
    # 实例化分页类
    p = Paginator(data,10) 

    # 获取当前的页码数
    pageindex=request.GET.get('page',1)

    # 获取当前页的数据
    userlist=p.page(pageindex)

    # 分配数据
    context = {'userdata':userlist}
    return render(request,'myadmin/auth/index.html',context)

# 权限管理 管理员添加
@permission_required('auth.add_group',raise_exception=True)
def myadmin_authuser_add(request):
    # 获取当前已经创建的所有 组
    gs = Group.objects.all()
    # 分配数据
    context = {'grouplist':gs}
    return render(request,'myadmin/auth/add.html',context)


# 权限管理 执行管理员添加
@permission_required('auth.add_group',raise_exception=True)
def myadmin_authuser_insert(request):
    # 接收数据
    data = request.POST.dict() 
    data.pop('csrfmiddlewaretoken')
    data.pop('gs')
    # 判断是否为超级会员
    if data['is_superuser'] == '1':
        data['is_superuser'] = True
        # 创建超级管理员
        ob = User.objects.create_superuser(**data)
    else:
        # 创建管理员
        ob = User.objects.create_user(**data)

    # 判断是否给当前用户分配了组
    gs = request.POST.getlist('gs')
    if gs:
        # 给当前管理员设置组
        ob.groups.set(gs)
        ob.save()

    return HttpResponse('<script>alert("创建成功");location.href="/myadmin/auth/user/index/"</script>')

def myadmin_authuser_edit(request):
    # 接收用户ID
    uid = request.GET.get('uid')
    # 获取当前会员对象
    ob = User.objects.get(id=uid)

    # 判断当前的请求方式
    if request.method == 'POST':
         # 执行更新
        # 判断密码是否更新
        password_now=request.POST.get('password',None)
        if password_now:
            # 更新密码
            ob.password=make_password(request.POST['password'],None,'pbkdf2_sha256')

        # 更新其他字段
        ob.username = request.POST.get('username')
        ob.email = request.POST.get('email') 
        # 判断是否有权限组
        gs = request.POST.getlist('gs',None)
        # 先清空权限组再添加
        ob.groups.clear()
        if gs:
            ob.groups.set(gs)   
            
        ob.save()

        return HttpResponse('<script>alert("修改成功");location.href="/myadmin/auth/user/index/"</script>')
    else:
        # 获取当前已经创建的所有 组
        gs = Group.objects.exclude(user=ob)
        # 显示编辑表单
        context={'uinfo':ob,'grouplist':gs}
        # 加载模板
        return render(request,'myadmin/auth/edit.html',context)


# 权限管理 权限组列表
@permission_required('auth.add_group',raise_exception=True)
def myadmin_authgroup_index(request):
    # 获取所有组
    groupdata = Group.objects.all()
    # 实例化分页类
    p = Paginator(groupdata,10) 

    # 获取当前的页码数
    pageindex=request.GET.get('page',1)

    # 获取当前页的数据
    userlist=p.page(pageindex)

    # 分配数据
    context = {'groupdata':userlist}
    
    return render(request,'myadmin/auth/groupindex.html',context)

# 权限管理 权限组添加
@permission_required('auth.add_group',raise_exception=True)
def myadmin_authgroup_add(request):
    # 读取所有权限信息
    # Permission.objects.all()
    # 读取所有权限信息,并排除以Can开头的系统默认生成权限
    perms = Permission.objects.exclude(name__istartswith='Can')
    # 分配数据
    context = {'perms':perms}
    # 加载模板
    return render(request,'myadmin/auth/groupadd.html',context)


# 权限管理 执行权限组添加
@permission_required('auth.add_group',raise_exception=True)
def myadmin_authgroup_insert(request):
    # 接收组名 
    name = request.POST.get('name')
    # 创建组
    g = Group(name = name)
    g.save()
    # 给组设置权限
    prms = request.POST.getlist('prms',None)
    # 判断是否需要给组添加权限
    if prms:
        g.permissions.set(prms)
        g.save()

    return HttpResponse('<script>alert("组创建成功！");location.href="/myadmin/auth/group/add/"</script>')

@permission_required('auth.add_group',raise_exception=True)
def myadmin_authgroup_edit(request):
    # 接收权限组ID
    uid = request.GET.get('uid')
    ob = Group.objects.get(id=uid)
    print(ob.id,ob)
     # 判断当前的请求方式
    if request.method == 'POST':
        ob.name = request.POST.get('name')
        # 给组设置权限
        gs = request.POST.getlist('gs',None)
        gs.permissions.clear()
        # 先清空权限组再添加
        print(gs)
        if gs:
            ob.permissions.set(gs)
        # ob.save()

        return HttpResponse('<script>alert("组修改成功！");location.href="/myadmin/auth/group/add/"</script>')
    else:
        # 获取权限信息，排除已选权限，再排除系统权限
        gs = Permission.objects.exclude(group=ob).exclude(name__istartswith='can')
        # 显示编辑表单
        context={'uinfo':ob,'grouplist':gs}
        # 加载模板
        return render(request,'myadmin/auth/groupedit.html',context)

    



# 登录页
def myadmin_login(request):

    # 加载页面
    return render(request,'myadmin/login.html')

def myadmin_dologin(request):
    
    # 验证验证码是否正确
    if request.session.get('verifycode').upper()  == request.POST.get('vcode').upper():
        # 检测用户和密码
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['AdminUser']={'username':user.username,'uid':user.id}
            return HttpResponse('<script>alert("欢迎登录!");location.href="/myadmin/index/"</script>')

        return HttpResponse('<script>alert("账号或密码错误");location.href="/myadmin/login/"</script>')

    else:
        return HttpResponse('<script>alert("验证码错误!");location.href="/myadmin/login/"</script>')
   
def myadmin_logout(request):
    del request.session['AdminUser']
    logout(request)
 

    return HttpResponse('<script>alert("退出成功!");location.href="/myadmin/login/"</script>')


def verifycode(request):
    #引入绘图模块
    from PIL import Image, ImageDraw, ImageFont
    #引入随机函数模块
    import random
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 34
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象
    # font = ImageFont.truetype('NotoSansCJK-Light.ttc', 18)
    font = ImageFont.truetype('Comfortaa-Regular.ttf', 18)
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((10, 8), rand_str[0], font=font, fill=fontcolor)
    draw.text((33, 8), rand_str[1], font=font, fill=fontcolor)
    draw.text((55, 8), rand_str[2], font=font, fill=fontcolor)
    draw.text((80, 8), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    #内存文件操作   
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')
