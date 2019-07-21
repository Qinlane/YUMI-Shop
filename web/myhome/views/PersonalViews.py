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
    return render(request,'myhome/Users/personal.html')

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
    return render(request,'myhome/Users/add.html')

# 执行添加地址
def myhome_address_doadd(request):
    uid = request.GET.get('uid')
    data = request.POST.dict()
    data.pop('csrfmiddlewaretoken')
    name = data['name']
    address = data['address']
    phone = data['phone']
    context = {'uid':uid,'name':name,'address':address,'phone':phone}
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
    context = {'data':lists}
    return render(request,'myhome/Users/collect.html',context)

# 个人信息页面
def myhome_information(request):
    uid = request.session['VipUser']['uid']
    data = Users.objects.filter(id=uid)
    context = {'data':data}
    return render(request,'myhome/Users/information.html',context)

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
            # 删除原头像
            os.remove(BASE_DIR+ob.pic_url)
            # ./static/uploads/1545033786.7237682.png   --ob.pic_url
            # /home/yc/py16/py16-project/web   ---BASE_DIR
            # 正在上传新头像
            ob.pic_url = uploads_pic(myfile)
        # 更新其他字段
        ob.nikename = request.POST.get('nikename')
        ob.email = request.POST.get('email')
        ob.phone = request.POST.get('phone')
        ob.age = request.POST.get('age')
        ob.sex = request.POST.get('sex')
        ob.save()
    request.session['VipUser'] = {'uid': ob.id, 'nikename': ob.nikename, 'phone': ob.phone, 'pic_url': ob.pic_url,'email':ob.email}
    return HttpResponse('<script>alert("修改成功");location.href="/personal/";</script>')

# 安全设置页面
def myhome_safety(request):
    return render(request,'myhome/Users/safety.html')

# 邮箱发送测试
def send_many_email(request):
    title = "测试"
    # content1 = "邮箱验证"
    email_template_name = 'myhome/Users/mailbox.html'
    email_from = settings.DEFAULT_FROM_EMAIL
    reciever1 = [
        '386362711@qq.com',
    ]
    data = {'data':1}
    # 邮件1
    t = loader.get_template(email_template_name)
    html_content = t.render(data)
    msg = EmailMultiAlternatives(title, html_content, email_from, reciever1)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    # send_mail(title, html_content, email_from, reciever1)
    return HttpResponse("发送好了")


# 我的信息页面
def myhome_news(request):
    return render(request,'myhome/Users/news.html')

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