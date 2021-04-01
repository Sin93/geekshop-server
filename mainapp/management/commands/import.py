from django.core.management import BaseCommand
from mainapp.models import ProductCategory, Product
from authapp.models import ShopUser, ShopUserProfile

import json


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        ShopUser.objects.create_superuser(username='django', email='', password='geekbrains')
        # Пользователь из персонала
        ShopUser.objects.create_user(username='staff', email='staff@mail.ru', password='staff', is_staff=True)
        # Простой пользователь
        ShopUser.objects.create_user(username='user', email='user@mail.ru', password='user')

        with open('mainapp/fixtures/categories.json', 'r') as file:
            categories = json.load(file)

        for category in categories:
            ProductCategory.objects.create(name=category['name'], url=category['url'], description=category['description'])

        with open('mainapp/fixtures/products.json', 'r') as file:
            products = json.load(file)

        for product in products:
            Product.objects.create(
                name=product['name'],
                short_desc=product['short_desc'],
                description=product['description'],
                price=product['price'],
                quantity=product['quantity'],
                category=ProductCategory.objects.get(pk=product['category'])
            )
