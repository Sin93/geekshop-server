from django.shortcuts import render, get_object_or_404
from mainapp.models import ProductCategory, Product
from basketapp.models import Basket

import os
import json


THIS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main(request):
    context = {
        'title': 'магазин'
    }
    context = add_basket_in_context(request, context)
    return render(request, 'mainapp/index.html', context)


def products(request, category=None):
    context = {
        'title': 'каталог',
        'category_url': category,
        'categories': ProductCategory.objects.all(),
    }

    if not category:
        context['products'] = Product.objects.all()
    else:
        category = get_object_or_404(ProductCategory, url=category)
        context['products'] = Product.objects.filter(category=category)

    context = add_basket_in_context(request, context)

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
    context = add_basket_in_context(request, context)

    return render(request, 'mainapp/contact.html', context)


def add_basket_in_context(request, context):
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
        context['basket'] = basket
        context['basket_sum'] = basket[0].total_cost() if basket else None
        return context
