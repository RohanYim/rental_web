# Generated by Django 3.2.6 on 2021-09-17 04:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0011_auto_20210917_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='bidorder',
            name='order_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 17, 12, 47, 36, 94254)),
        ),
        migrations.AddField(
            model_name='bidorder',
            name='remove_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 17, 12, 47, 36, 94254)),
        ),
    ]
