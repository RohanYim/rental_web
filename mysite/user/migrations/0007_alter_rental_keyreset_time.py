# Generated by Django 3.2.6 on 2021-09-20 02:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_rental_keyreset_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rental',
            name='keyreset_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 20, 10, 37, 21, 850925)),
        ),
    ]
