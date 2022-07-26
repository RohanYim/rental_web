# Generated by Django 3.2.6 on 2021-09-18 06:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0021_auto_20210918_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='bidorder',
            name='alipay_no',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='bidorder',
            name='order_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 18, 14, 0, 18, 95186)),
        ),
        migrations.AlterField(
            model_name='bidorder',
            name='remove_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 18, 14, 0, 18, 95186)),
        ),
        migrations.AlterField(
            model_name='botbidding',
            name='order_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 18, 14, 0, 18, 94189)),
        ),
        migrations.AlterField(
            model_name='botbidding',
            name='remove_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 18, 14, 0, 18, 94189)),
        ),
    ]
