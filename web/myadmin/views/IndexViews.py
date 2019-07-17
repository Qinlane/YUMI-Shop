from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import Users


# Create your views here.

def index(request):
    
    return render(request,'myadmin/index.html')

# 登录页
def myadmin_login(request):

    # 加载页面
    return render(request,'myadmin/login.html')

def myadmin_dologin(request):
    
    # 验证验证码是否正确
    if request.session.get('verifycode').upper()  == request.POST.get('vcode').upper():
        if request.POST['username']== 'admin' and request.POST['password'] == '123654':
            request.session['AdminUser']={'username':'admin','uid':10}
            return HttpResponse('<script>alert("欢迎登录!");location.href="/myadmin/index/"</script>')
        else:
            return HttpResponse('<script>alert("账号或密码错误");location.href="/myadmin/login/"</script>')

    else:
        return HttpResponse('<script>alert("验证码错误!");location.href="/myadmin/login/"</script>')
   

    # # 验证验证码是否正确
    # if request.session.get('verifycode').upper()  == request.POST.get('vcode').upper():
    #     # 验证账号是否存在
    #     ob = Users.objects.get(nikename=request.POST['nikename'])
    #     res = check_password(request.POST['password'],ob.password)
    #     if res:
    #         # 验证成功
    #         request.session['AdminUser']={'username':nikename,'uid':}
    #         return HttpResponse('<script>alert("欢迎登录!");location.href="/myadmin/index/"</script>')

    #     else:
    #         return HttpResponse('<script>alert("账号或密码错误");location.href="/myadmin/login/"</script>')

    # else:
    #     return HttpResponse('<script>alert("验证码错误!");location.href="/myadmin/login/"</script>')


def myadmin_logout(request):
    del request.session['AdminUser']

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
