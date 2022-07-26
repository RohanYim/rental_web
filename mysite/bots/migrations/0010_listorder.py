# Generated by Django 3.2.6 on 2021-09-16 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0009_bidorder'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buyer_id', models.CharField(default='', max_length=30)),
                ('status', models.CharField(choices=[('Unpaid', 'Unpaid'), ('Paid', 'Paid')], default='Unpaid', max_length=15)),
                ('list_pk', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bots.botlisting')),
            ],
        ),
    ]
