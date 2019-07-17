from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.hashers import make_password,check_password
from myadmin.models import Users

# 显示登陆页面
def myhome_login(request):
    return render(request,'myhome/login/login.html')

# 执行登陆
def myhome_dologin(request):
    try:
        # 验证手机号是否存在
        ob = Users.objects.get(phone=request.POST['phone'])
        # 验证密码
        res = check_password(request.POST['password'],ob.password)
        if res:
            request.session['VipUser'] = {'uid':ob.id,'nikename':ob.nikename,'phone':ob.phone,'pic_url':ob.pic_url}
            return HttpResponse('<script>alert("登陆成功");location.href="/";</script>')
    except:
        pass
    return HttpResponse('<script>alert("手机号或密码不正确");history.back(-1)</script>')

# 退出登陆
def myhome_logout(request):
    del request.session['VipUser']
    return HttpResponse('<script>alert("退出登录");location.href="/";</script>')

# 显示注册页面
def myhome_register(request):
    return render(request, 'myhome/login/register.html')

# 执行注册
def myhome_doregister(request):
    try:
        # 接收表单数据
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')
        data.pop('againpassword')

        # 验证手机验证码是否正确
        if data['vcode'] == request.session['msgcode']['code'] and data['phone'] == request.session['msgcode']['phone']:
            data.pop('vcode')
            # 验证手机号是否存在
            res = Users.objects.filter(phone=data['phone']).count()
            # 手机号已存在
            if res:
                return HttpResponse('<script>alert("该手机号已被注册");history.back(-1)</script>')

            data['password'] = make_password(data['password'],None,'pbkdf2_sha256')

            ob = Users(**data)
            ob.save()
            return HttpResponse('<script>alert("注册成功，请登陆");location.href="/login/";</script>')
        else:
            return HttpResponse('<script>alert("手机验证码错误");history.back(-1)</script>')
    except:
        pass

    return HttpResponse('<script>alert("注册失败，请联系相关工作人员");history.back(-1)</script>')

# 短信验证
def myhome_sendMsg(request):
    import random
    phone = request.GET.get('phone')
    # 随机验证码
    code = str(random.randint(1000, 9999))
    # 把验证码存入session
    request.session['msgcode'] = {'code': code, 'phone': phone}
    # 调用方法 发送短信验证
    res = hywx_send(phone, code)
    return JsonResponse(res)

# 生成短信验证
def hywx_send(mobile, code):
    # 接口类型：互亿无线触发短信接口，支持发送验证码短信、订单通知短信等。
    # 账户注册：请通过该地址开通账户http://user.ihuyi.com/register.html
    # 注意事项：
    # （1）调试期间，请用默认的模板进行测试，默认模板详见接口文档；
    # （2）请使用 用户名 及 APIkey来调用接口，APIkey在会员中心可以获取；
    # （3）该代码仅供接入互亿无线短信接口参考使用，客户可根据实际需要自行编写；
    import urllib
    import urllib.request
    import json

    # 用户名 查看用户名请登录用户中心->验证码、通知短信->帐户及签名设置->APIID
    # account = "C44710327"
    # # 密码 查看密码请登录用户中心->验证码、通知短信->帐户及签名设置->APIKEY
    # password = "536d4ec71831f8686b2e7326b60fe0e3"
    # mobile = request.GET.get('phone')

    text = "您的验证码是：" + code + "。请不要把验证码泄露给其他人。"
    # data = {'account': account, 'password': password, 'content': text, 'mobile': mobile, 'format': 'json'}
    # req = urllib.request.urlopen(
    #     url= 'http://106.ihuyi.com/webservice/sms.php?method=Submit',
    #     data= urllib.parse.urlencode(data).encode('utf-8')
    # )
    # 获取接口响应的内容
    # content = req.read()
    # res = json.loads(content.decode('utf-8'))

    res = {'code': 2, 'msg': '提交成功', 'id': '1111', 'yzm': code}
    return res

# 手机号是否被注册
def isphone(request):
    phone = request.GET.get('phone')
    ob = Users.objects.all()
    if ob.filter(phone__contains=phone):
        return JsonResponse({'res':1})
    else:
        return JsonResponse({'res':0})