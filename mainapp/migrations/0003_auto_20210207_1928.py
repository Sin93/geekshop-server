# Generated by Django 2.2.17 on 2021-02-07 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_productcategory_url'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name_plural': 'Товары'},
        ),
        migrations.AlterModelOptions(
            name='productcategory',
            options={'verbose_name_plural': 'Категории'},
        ),
    ]
