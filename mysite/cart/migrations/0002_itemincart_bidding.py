# Generated by Django 3.2.6 on 2021-09-16 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0008_auto_20210916_1408'),
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemincart',
            name='bidding',
            field=models.ManyToManyField(default='', to='bots.BotBidding'),
        ),
    ]
