# Generated by Django 3.2.6 on 2021-09-16 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0006_botbidding_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='botbidding',
            name='deposit_order_no',
            field=models.CharField(default='', max_length=15),
        ),
    ]
