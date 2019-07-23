from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.hashers import make_password,check_password
from myadmin.models import Users,Goods
from myhome.models import Address,Collect
from web.settings import BASE_DIR
import os
from django.core.mail import send_mail,EmailMultiAlternatives
from web import settings
from django.template import loader


# 个人中心首页
def myhome_personal(request):
    uid = request.session['VipUser']['uid']
    ob = Users.objects.get(id=uid)
    context = {'data':ob}
    return render(request,'myhome/Users/personal.html',context)

# 地址管理
def myhome_address(request):
    type = request.session['VipUser']['uid']
    ob = Address.objects.filter(uid__contains=type)
    count = Address.objects.filter(uid__contains=type).count()
    context = {'ob':ob,'count':count}
    return render(request,'myhome/Users/address.html',context)

# 设为默认地址
def myhome_address_def(request):
    id = request.GET.get('id')
    uid = request.GET.get('uid')
    Address.objects.filter(uid=uid).update(status=1)
    Address.objects.filter(id=id).update(status=0)
    return HttpResponse('<script>alert("设置成功");location.href="/address/";</script>')

# 添加地址页面
def myhome_address_add(request):
    uid = request.session['VipUser']['uid']
    ob = Users.objects.get(id=uid)
    context = {'data':ob}
    return render(request,'myhome/Users/add.html',context)

# 执行添加地址
def myhome_address_doadd(request):
    uid = request.session['VipUser']['uid']
    data = request.POST.dict()
    data.pop('csrfmiddlewaretoken')
    name = data['name']
    address = data['address']
    phone = data['phone']
    context = {'uid':uid,'name':name,'address':address,'phone':phone,'status':0}
    Address.objects.filter(uid=uid).update(status=1)
    ob = Address(**context)
    ob.save()
    return HttpResponse('<script>alert("添加成功");location.href="/address/";</script>')

# 编辑收货地址页面
def myhome_address_edit(request):
    vid = request.GET.get('vid')
    data = Address.objects.filter(id=vid)
    context = {'data':data}
    return render(request,'myhome/Users/edit.html',context)

# 执行编辑操作
def myhome_address_doedit(request):
    id = request.GET.get('id')
    data = request.POST.dict()
    data.pop('csrfmiddlewaretoken')
    Address.objects.filter(id=id).update(name=data['name'],address=data['address'],phone=data['phone'])
    return HttpResponse('<script>alert("编辑成功");location.href="/address/";</script>')

# 删除收货地址
def myhome_address_del(request):
    vid = request.GET.get('vid')
    Address.objects.filter(id=vid).delete()
    return HttpResponse('<script>alert("删除成功");location.href="/address/";</script>')

# 收藏页面
def myhome_collect(request):
    uid = request.session['VipUser']['uid']
    data = Collect.objects.filter(uid=uid)
    lists = []
    for i in data:
        ob = Goods.objects.filter(id=i.sid)
        lists += ob
    context = {'lists':lists}
    return render(request,'myhome/Users/collect.html',context)

# 删除收藏商品操作
def myhome_collect_del(request):
    from django.db.models import Q
    uid = request.session['VipUser']['uid']
    sid = request.POST.getlist('check_item')
    print(sid)
    for i in sid:
        Collect.objects.filter(Q(uid__contains=uid)&Q(sid__contains=i)).delete()
    return HttpResponse('<script>alert("删除成功");history.back(-1);</script>')

# 个人信息页面
def myhome_information(request):
    uid = request.session['VipUser']['uid']
    data = Users.objects.filter(id=uid)
    context = {'data':data}
    return render(request,'myhome/Users/information.html',context)

# 修改个人信息页面
def myhome_doinfor(request):
    # 接收用户ID
    uid = request.session['VipUser']['uid']
    # 获取当前会员对象
    ob = Users.objects.get(id=uid)
    # 判断当前的请求方式
    if request.method == 'POST':
        # 执行更新
        myfile = request.FILES.get('pic',None)
        if myfile:
            if ob.pic_url:
                # 删除原头像
                os.remove(BASE_DIR+ob.pic_url)
            # ./static/uploads/1545033786.7237682.png   --ob.pic_url
            # /home/yc/py16/py16-project/web   ---BASE_DIR
            # 正在上传新头像
            ob.pic_url = uploads_pic(myfile)
        # 更新其他字段
        ob.nikename = request.POST.get('nikename')
        ob.age = request.POST.get('age')
        ob.sex = request.POST.get('sex')
        ob.save()
    return HttpResponse('<script>alert("修改成功");location.href="/personal/";</script>')

# 安全设置页面
def myhome_safety(request):
    uid = request.session['VipUser']['uid']
    ob = Users.objects.get(id=uid)
    context = {'data':ob}
    return render(request,'myhome/Users/safety.html',context)

# 修改密码页面
def myhome_password(request):
    return render(request,'myhome/Users/password.html')

# 执行密码修改
def myhome_passwordmol(request):
    uid = request.session['VipUser']['uid']
    ob = Users.objects.get(id=uid)
    data = request.POST.dict()
    data.pop('csrfmiddlewaretoken')
    if(data['newpassword']!=data['againpassword']):
        return HttpResponse('<script>alert("修改失败，2次密码输入不一致");history.back(-1);</script>')
    #     check_password 第一个参数为明文，第二个参数为密文
    elif(check_password(data['password'],ob.password)):
        ob.password = make_password(data['newpassword'])
        ob.save()
        return HttpResponse('<script>alert("修改成功");location.href="/safety/";</script>')
    else:
        return HttpResponse('<script>alert("修改失败，原密码输入错误");history.back(-1);</script>')

# 换绑手机号页面
def myhome_phone(request):
    return render(request,'myhome/Users/phone.html')

# 执行手机号更换
def myhome_phone_change(request):
    uid = request.session['VipUser']['uid']
    data = request.POST.dict()
    ob = Users.objects.get(id=uid)
    if(data['vcode'] == request.session['msgcode']['code'] and data['phone'] == request.session['msgcode']['phone']):
        data.pop('vcode')
        res = Users.objects.filter(phone=data['phone']).count()
        # 手机号已存在
        if res:
            return HttpResponse('<script>alert("该手机号已被注册");history.back(-1)</script>')
        ob.phone = request.POST.get('phone')
        ob.save()
        return HttpResponse('<script>alert("修改成功");location.href="/safety/";</script>')
    else:
        pass
    return HttpResponse('<script>alert("验证码不正确");history.back(-1)</script>')

# 邮箱绑定页面
def myhome_email(request):
    return render(request,'myhome/Users/email.html')

# 执行邮箱绑定
def myhome_email_bind(request):
    uid = request.session['VipUser']['uid']
    data = request.POST.dict()
    ob = Users.objects.get(id=uid)
    if (data['vcode'] == request.session['msgcode']['code'] and data['email'] == request.session['msgcode'][
        'email']):
        data.pop('vcode')
        res = Users.objects.filter(phone=data['email']).count()
        # 手机号已存在
        if res:
            return HttpResponse('<script>alert("该邮箱已被注册");history.back(-1)</script>')
        ob.email = request.POST.get('email')
        ob.save()
        return HttpResponse('<script>alert("绑定成功");location.href="/safety/";</script>')
    else:
        pass
    return HttpResponse('<script>alert("验证码不正确");history.back(-1)</script>')

# 邮箱发送
def myhome_email_html(request):
    title = "鱼咪网购"
    import random
    email = request.GET.get('email')
    # 随机验证码
    code = str(random.randint(100000, 999999))
    # 把验证码存入session
    request.session['msgcode'] = {'code': code, 'email': email}
    email_template = 'myhome/Users/mailbox.html'
    email_from = settings.DEFAULT_FROM_EMAIL
    reciever = [
        email,
    ]
    data = {'code':code}
    # html邮件
    t = loader.get_template(email_template)
    html_content = t.render(data)
    msg = EmailMultiAlternatives(title, html_content, email_from, reciever)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    # send_mail(title, html_content, email_from, reciever1)
    return JsonResponse(data)

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