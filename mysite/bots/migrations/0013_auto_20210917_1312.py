# Generated by Django 3.2.6 on 2021-09-17 05:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0012_auto_20210917_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidorder',
            name='order_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 17, 13, 12, 17, 953399)),
        ),
        migrations.AlterField(
            model_name='bidorder',
            name='remove_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 17, 13, 12, 17, 953399)),
        ),
    ]
