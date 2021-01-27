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
    context = {
        'title': 'каталог'
    }
    return render(request, 'mainapp/products.html', context)


def contact(request):
    with open(f'{THIS_DIR}\contact.json', 'r') as read_file:
        contacts_list = json.load(read_file)

    context = {
        'title': 'Контакты',
        'contacts': contacts_list
    }
    return render(request, 'mainapp/contact.html', context)
