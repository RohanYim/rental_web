# Generated by Django 3.2.6 on 2021-09-16 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0005_botbidding'),
    ]

    operations = [
        migrations.AddField(
            model_name='botbidding',
            name='payment_status',
            field=models.CharField(choices=[('Unpaid', 'Unpaid'), ('Paid', 'Paid')], default='Unpaid', max_length=15),
        ),
    ]
