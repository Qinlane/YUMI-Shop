# Generated by Django 2.2.2 on 2019-07-24 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0003_auto_20190724_1622'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='users',
            options={'permissions': (('show_Uswrs', '查看用户列表权限'), ('create_Users', '添加用户信息权限'), ('edit_Users', '修改用户信息权限'), ('remove_Users', '删除用户信息权限'))},
        ),
        migrations.AlterField(
            model_name='users',
            name='sex',
            field=models.CharField(choices=[(0, '女'), (1, '男')], max_length=1, null=True),
        ),
    ]