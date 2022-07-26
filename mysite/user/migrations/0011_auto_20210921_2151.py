# Generated by Django 3.2.6 on 2021-09-21 13:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_auto_20210921_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='alipay_id',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='rental',
            name='keyreset_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 21, 21, 51, 37, 729211)),
        ),
        migrations.AlterField(
            model_name='rental',
            name='request_time',
            field=models.CharField(default=datetime.datetime(2021, 9, 21, 21, 51, 37, 729211), max_length=200),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('Paid', 'Paid'), ('Processing', 'Processing'), ('Failed', 'Failed')], default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='use',
            field=models.CharField(choices=[('topup', 'topup'), ('withdrawal', 'withdrawal'), ('Refund', 'Refund')], default='', max_length=20),
        ),
    ]
