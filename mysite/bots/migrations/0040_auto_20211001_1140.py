# Generated by Django 3.2.6 on 2021-10-01 03:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0039_auto_20210929_1056'),
    ]

    operations = [
        migrations.RenameField(
            model_name='botbidding',
            old_name='price',
            new_name='rmb_price',
        ),
        migrations.AddField(
            model_name='botbidding',
            name='usd_price',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='bidorder',
            name='order_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 1, 11, 40, 37, 814931)),
        ),
        migrations.AlterField(
            model_name='bidorder',
            name='remove_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 1, 11, 40, 37, 814931)),
        ),
        migrations.AlterField(
            model_name='botbidding',
            name='keyreset_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 1, 11, 40, 37, 812936)),
        ),
        migrations.AlterField(
            model_name='botbidding',
            name='order_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 1, 11, 40, 37, 812936)),
        ),
        migrations.AlterField(
            model_name='botbidding',
            name='remove_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 1, 11, 40, 37, 812936)),
        ),
        migrations.AlterField(
            model_name='botbidding',
            name='request_time',
            field=models.CharField(default=datetime.datetime(2021, 10, 1, 11, 40, 37, 812936), max_length=200),
        ),
        migrations.AlterField(
            model_name='botlisting',
            name='key',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='botlisting',
            name='keyreset_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 1, 11, 40, 37, 811939)),
        ),
        migrations.AlterField(
            model_name='botlisting',
            name='request_time',
            field=models.CharField(default=datetime.datetime(2021, 10, 1, 11, 40, 37, 811939), max_length=200),
        ),
    ]
