from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from mainapp.models import ProductCategory, Product

import os
import json


THIS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MESSAGES = {
    'successful_register': 'Вы успешно зарегистрировались. На вашу почту отправлено письмо со ссылкой для подтверждения регистрации.',
    'successful_verify': 'E-mail подтверждён, регистрация успешно завершена.'
}


def main(request, message=None):
    context = {
        'title': 'магазин'
    }

    if message:
        context['message'] = MESSAGES[message]

    return render(request, 'mainapp/index.html', context)


def products(request, category=None, page=1):
    """В данном проекте сделано таким образом, что товар не может быть активен,
    если деактивирована категория. По этому проверку на активность категории
    не делаю"""
    if not category:
        products = Product.objects.filter(is_active=True).order_by('price')
    else:
        category = get_object_or_404(ProductCategory, url=category)
        products = Product.objects.filter(
            category=category,
            is_active=True
        ).order_by('price')

    paginator = Paginator(products, 3)

    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context = {
        'title': 'каталог',
        'category_url': category,
        'categories': ProductCategory.objects.filter(is_active=True),
        'products': products_paginator,
        'current_page': page,
    }

    return render(request, 'mainapp/products.html', context)


def view_product(request, id):
    product = get_object_or_404(Product, pk=id)
    context = {
        'title': product.name,
        'data': product
    }
    return render(request, 'mainapp/product.html', context)


def contact(request):
    with open(os.path.join(THIS_DIR, 'mainapp', 'fixtures', 'contacts.json'), 'r') as read_file:
        contacts_list = json.load(read_file)

    context = {
        'title': 'Контакты',
        'contacts': contacts_list,
    }

    return render(request, 'mainapp/contact.html', context)
