from django.db import models

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
