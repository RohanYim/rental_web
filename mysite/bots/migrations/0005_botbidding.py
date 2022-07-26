# Generated by Django 3.2.6 on 2021-09-15 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0004_auto_20210915_1411'),
    ]

    operations = [
        migrations.CreateModel(
            name='BotBidding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(default='', max_length=25)),
                ('bot', models.CharField(default='', max_length=25)),
                ('img_url', models.CharField(default='', max_length=100)),
                ('listing_type', models.CharField(default='', max_length=30)),
                ('start_time', models.CharField(default='', max_length=200)),
                ('end_time', models.CharField(default='', max_length=200)),
                ('price', models.FloatField(default=0.0)),
                ('status', models.CharField(choices=[('Show', 'Show'), ('Unshow', 'Unshow')], default='Show', max_length=15)),
            ],
        ),
    ]
