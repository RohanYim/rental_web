# Generated by Django 3.2.6 on 2021-09-20 03:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0030_auto_20210920_1037'),
    ]

    operations = [
        migrations.AddField(
            model_name='botbidding',
            name='keyreset_status',
            field=models.CharField(choices=[('Waiting for reset', 'Waiting for reset'), ('Nothing', 'Nothing')], default='Nothing', max_length=30),
        ),
        migrations.AddField(
            model_name='botbidding',
            name='keyreset_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 20, 11, 47, 31, 517749)),
        ),
        migrations.AlterField(
            model_name='bidorder',
            name='order_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 20, 11, 47, 31, 518747)),
        ),
        migrations.AlterField(
            model_name='bidorder',
            name='remove_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 20, 11, 47, 31, 518747)),
        ),
        migrations.AlterField(
            model_name='botbidding',
            name='order_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 20, 11, 47, 31, 517749)),
        ),
        migrations.AlterField(
            model_name='botbidding',
            name='remove_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 20, 11, 47, 31, 517749)),
        ),
        migrations.AlterField(
            model_name='botlisting',
            name='keyreset_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 20, 11, 47, 31, 516752)),
        ),
    ]
