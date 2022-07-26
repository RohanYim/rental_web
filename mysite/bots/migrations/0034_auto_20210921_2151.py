# Generated by Django 3.2.6 on 2021-09-21 13:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0033_auto_20210921_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidorder',
            name='order_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 21, 21, 51, 37, 735192)),
        ),
        migrations.AlterField(
            model_name='bidorder',
            name='remove_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 21, 21, 51, 37, 735192)),
        ),
        migrations.AlterField(
            model_name='botbidding',
            name='keyreset_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 21, 21, 51, 37, 734197)),
        ),
        migrations.AlterField(
            model_name='botbidding',
            name='order_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 21, 21, 51, 37, 734197)),
        ),
        migrations.AlterField(
            model_name='botbidding',
            name='remove_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 21, 21, 51, 37, 734197)),
        ),
        migrations.AlterField(
            model_name='botbidding',
            name='request_time',
            field=models.CharField(default=datetime.datetime(2021, 9, 21, 21, 51, 37, 734197), max_length=200),
        ),
        migrations.AlterField(
            model_name='botlisting',
            name='keyreset_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 21, 21, 51, 37, 734197)),
        ),
        migrations.AlterField(
            model_name='botlisting',
            name='request_time',
            field=models.CharField(default=datetime.datetime(2021, 9, 21, 21, 51, 37, 734197), max_length=200),
        ),
    ]
