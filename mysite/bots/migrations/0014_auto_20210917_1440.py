# Generated by Django 3.2.6 on 2021-09-17 06:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0013_auto_20210917_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='botbidding',
            name='order_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 17, 14, 40, 39, 73473)),
        ),
        migrations.AddField(
            model_name='botbidding',
            name='remove_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 17, 14, 40, 39, 73473)),
        ),
        migrations.AlterField(
            model_name='bidorder',
            name='order_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 17, 14, 40, 39, 74472)),
        ),
        migrations.AlterField(
            model_name='bidorder',
            name='remove_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 17, 14, 40, 39, 74472)),
        ),
    ]
