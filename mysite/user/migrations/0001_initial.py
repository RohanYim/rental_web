# Generated by Django 3.2.6 on 2021-09-15 05:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buyer_id', models.CharField(default='', max_length=20)),
                ('seller_id', models.CharField(default='', max_length=20)),
                ('listing_num', models.PositiveIntegerField(default=0)),
                ('keyreset_status', models.CharField(choices=[('Waiting for reset', 'Waiting for reset'), ('Nothing', 'Nothing')], default='Nothing', max_length=30)),
                ('rental_status', models.CharField(choices=[('Active', 'Active'), ('Upcoming', 'Upcoming'), ('Past', 'Past')], default='', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Verify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(default='', max_length=20)),
                ('user_discord', models.CharField(default='', max_length=30)),
                ('bot', models.CharField(default='', max_length=15)),
                ('key', models.CharField(default='', max_length=200)),
                ('key_nickname', models.CharField(default='', max_length=20)),
                ('status', models.CharField(choices=[('Processing Verification', 'Processing Verification'), ('Ready to be listed', 'Ready to be listed'), ('Not Verified', 'Not Verified'), ('Listed', 'Listed')], default='Processing Verification', max_length=30)),
                ('need_reset', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.FloatField(default=0.0)),
                ('withdraw_able', models.FloatField(default=0.0)),
                ('freeze', models.FloatField(default=0.0)),
                ('points', models.FloatField(default=0.0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sell_count', models.PositiveIntegerField(default=0)),
                ('level', models.PositiveIntegerField(default=1)),
                ('seller_fee', models.FloatField(default=20.0)),
                ('warning', models.PositiveIntegerField(default=0)),
                ('twitter_link', models.CharField(default='', max_length=200)),
                ('Refs', models.PositiveIntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discordname', models.CharField(default='', max_length=20)),
                ('discordid', models.CharField(default='', max_length=20)),
                ('connected', models.BooleanField(default=False)),
                ('timezone', models.CharField(choices=[('GMT+8', 'GMT+8(Asia)'), ('GMT-4', 'GMT-4(North America)'), ('GMT+1', 'GMT+1(Europe)')], default='GMT+8', max_length=15)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buy_count', models.PositiveIntegerField(default=0)),
                ('level', models.PositiveIntegerField(default=1)),
                ('points', models.FloatField(default=0.0)),
                ('buyer_fee', models.FloatField(default=10.0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BotInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(default='', max_length=20)),
                ('user_discord', models.CharField(default='', max_length=30)),
                ('bot', models.CharField(choices=[('Dashe', 'Dashe'), ('Cyber', 'Cyber'), ('Balko', 'Balko')], default='', max_length=15)),
                ('key', models.CharField(default='', max_length=200)),
                ('key_nickname', models.CharField(default='', max_length=200)),
                ('status', models.CharField(choices=[('Processing Verification', 'Processing Verification'), ('Ready to be listed', 'Ready to be listed'), ('Not Verified', 'Not Verified'), ('Listed', 'Listed')], default='Processing Verification', max_length=30)),
                ('need_reset', models.BooleanField(default=False)),
            ],
            options={
                'unique_together': {('user_discord', 'key')},
            },
        ),
    ]
