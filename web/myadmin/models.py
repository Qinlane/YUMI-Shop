from django.db import models

# Create your models here.


# 定义会员模型
class Users(models.Model):
    nikename = models.CharField(max_length=20,null=True)
    password = models.CharField(max_length=80)
    phone = models.CharField(max_length=11)
    email = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    pic_url = models.CharField(max_length=100)
    SEX_CHOICES = {
        (0,'女'),
        (1,'男'),
    }
    sex = models.CharField(max_length=1,null=True,choices=SEX_CHOICES)
    # 0 正常 1 禁用 2 删除 ...
    status = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)

# 商品分类模型
class Cates(models.Model):
    name = models.CharField(max_length=20)
    pid = models.IntegerField()
    path = models.CharField(max_length=50)

# 商品模型
class Goods(models.Model):
    # id 所属分类，商品名，图片，添加时间，销量

    cateid = models.ForeignKey(to="Cates",to_field="id",on_delete=models.CASCADE)
    goodsname = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    brand = models.CharField(max_length=50)
    color = models.CharField(max_length=50,default="")
    sizes = models.CharField(max_length=50,default="")
    price = models.FloatField()
    goodsnum = models.IntegerField()
    pic_url = models.CharField(max_length=255)
    goodsinfo = models.TextField()
    ordernum = models.IntegerField(default=0)
    clicknum = models.IntegerField(default=0)
    #0新品 1热卖 2推荐 3下架
    status = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)

# 购物车 模型
class Cart(models.Model):
    #  id 用户 uid 商品 goodsid 数量 num
    uid = models.ForeignKey(to="Users",to_field="id",on_delete=models.CASCADE)
    color = models.CharField(max_length=11,default="")
    sizes = models.CharField(max_length=20,default="")
    goodsid = models.ForeignKey(to="Goods",to_field="id",on_delete=models.CASCADE)
    num = models.IntegerField()