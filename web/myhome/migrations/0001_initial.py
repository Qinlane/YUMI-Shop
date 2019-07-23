# Generated by Django 2.2.2 on 2019-07-23 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.IntegerField()),
                ('name', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=11)),
                ('status', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Collect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.IntegerField()),
                ('sid', models.IntegerField()),
            ],
        ),
    ]
