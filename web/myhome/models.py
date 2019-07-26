from django.db import models
from myadmin.models import Cates,Goods,Cart,Users


# 地址管理模型
class Address(models.Model):
    uid = models.IntegerField()
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=11)
    status = models.IntegerField()

# 个人中心收藏模型
class Collect(models.Model):
    uid = models.IntegerField()
    sid = models.IntegerField()
# Create your models here.

# 第三方登录用户信息模型
class OAuth_ex(models.Model):
    type = models.IntegerField(default=1)  # 1状态为github登录
    user = models.ForeignKey(Users)
    openid = models.CharField(max_length=100, default='')