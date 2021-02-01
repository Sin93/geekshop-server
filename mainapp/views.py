from django.shortcuts import render, get_object_or_404
from mainapp.models import ProductCategory, Product

import os
import json


THIS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main(request):
    context = {
        'title': 'магазин'
    }
    return render(request, 'mainapp/index.html', context)


def products(request, category=None):
    context = {
        'title': 'каталог',
        'categories': ProductCategory.objects.all(),
    }

    if not category:
        context['products'] = Product.objects.all()
    else:
        category = get_object_or_404(ProductCategory, url=category)
        context['products'] = Product.objects.filter(category=category)

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
