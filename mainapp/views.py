from django.shortcuts import render

import os
import json


THIS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main(request):
    context = {
        'title': 'магазин'
    }
    return render(request, 'mainapp/index.html', context)


def products(request):
    with open(os.path.join(THIS_DIR, 'products.json'), 'r') as file:
        products = json.load(file)

    context = {
        'title': 'каталог',
        'products': products,
    }
    return render(request, 'mainapp/products.html', context)


def view_product(request, id):
    with open(os.path.join(THIS_DIR, 'products.json'), 'r') as file:
        products = json.load(file)
    for product in products:
        if int(product['id']) == id:
            data = product
            break
    context = {
        'title': data['name'],
        'data': data
    }
    return render(request, 'mainapp/product.html', context)

def contact(request):
    with open(os.path.join(THIS_DIR, 'contacts.json'), 'r') as read_file:
        contacts_list = json.load(read_file)

    context = {
        'title': 'Контакты',
        'contacts': contacts_list,
    }
    return render(request, 'mainapp/contact.html', context)
