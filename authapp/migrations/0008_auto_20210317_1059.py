# Generated by Django 3.1.7 on 2021-03-17 07:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0007_auto_20210316_0931'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopuserprofile',
            name='language',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Язык'),
        ),
        migrations.AddField(
            model_name='shopuserprofile',
            name='vk_url',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Ссылка на профиль'),
        ),
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 19, 7, 59, 37, 307475, tzinfo=utc)),
        ),
    ]