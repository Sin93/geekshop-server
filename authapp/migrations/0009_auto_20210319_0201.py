# Generated by Django 3.1.7 on 2021-03-18 23:01

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0008_auto_20210317_1059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 20, 23, 1, 2, 197919, tzinfo=utc)),
        ),
    ]
