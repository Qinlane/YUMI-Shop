# Generated by Django 2.2.2 on 2019-07-24 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0002_auto_20190724_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='sex',
            field=models.CharField(choices=[(1, '男'), (0, '女')], max_length=1, null=True),
        ),
    ]
