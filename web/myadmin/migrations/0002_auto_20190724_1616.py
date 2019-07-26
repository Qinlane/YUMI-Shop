# Generated by Django 2.2.2 on 2019-07-24 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cates',
            options={'permissions': (('show_Cates', '查看分类列表权限'), ('create_Cates', '添加分类信息权限'), ('edit_Cates', '修改分类信息权限'), ('remove_Cates', '删除分类信息权限'))},
        ),
        migrations.AlterModelOptions(
            name='goods',
            options={'permissions': (('show_Goods', '查看商品列表权限'), ('create_Goods', '添加商品信息权限'), ('edit_Goods', '修改商品信息权限'), ('remove_Goods', '删除商品信息权限'))},
        ),
        migrations.AlterModelOptions(
            name='orderinfo',
            options={'permissions': (('show_Order', '查看订单列表权限'), ('create_Order', '添加订单信息权限'), ('edit_Order', '修改订单信息权限'), ('remove_Order', '删除订单信息权限'))},
        ),
        migrations.AlterModelOptions(
            name='users',
            options={'permissions': (('show_Uswrs', '查看用户列表权限'), ('create_Users', '添加用户信息权限'), ('edit_Cates', '修改分类信息权限'), ('remove_Cates', '删除分类信息权限'))},
        ),
        migrations.AlterField(
            model_name='users',
            name='sex',
            field=models.CharField(choices=[(0, '女'), (1, '男')], max_length=1, null=True),
        ),
    ]
