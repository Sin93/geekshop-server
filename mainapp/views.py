# Django
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.utils.translation import gettext as _
# Project
from mainapp.models import ProductCategory, Product

import os
import json


THIS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURES_DIR = os.path.join(THIS_DIR, 'mainapp', 'fixtures')
MESSAGES = {
    'successful_register': 'Вы успешно зарегистрировались. На вашу почту отправлено письмо со ссылкой для подтверждения регистрации.',
    'successful_verify': 'E-mail подтверждён, регистрация успешно завершена.'
}


class MainView(View):
    """Контроллер для отображения главной страницы"""
    title = 'магазин'
    template_name = 'mainapp/index.html'
    model = Product

    def queryset(self):
        return self.model.objects.order_by('?')[:4]

    def get_context_data(self, message=None, **kwargs):
        context = {
            'title': self.title,
            'object_list': self.queryset,
        }

        if message:
            context['message'] = MESSAGES[message]

        return context

    def get(self, request, message=None):
        return render(request, self.template_name, self.get_context_data(message))


class ProductListView(ListView):
    """Контроллер для отображения всех товаров в каталоге"""
    title = 'каталог'
    template_name = 'mainapp/products.html'
    model = Product
    paginate_by = 3
    paginator_class = Paginator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['categories'] = ProductCategory.objects.filter(is_active=True)
        return context

    def get_queryset(self):
        return Product.objects.all()


class CategoryProductListView(ProductListView):
    """Контроллер для отображения всех товаров выбранной категории"""
    category = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.category:
            context['category_url'] = self.category.url
        return context

    def get_queryset(self):
        return Product.objects.filter(category=self.category, is_active=True)

    def get(self, request, category=None, **kwargs):
        self.category = get_object_or_404(ProductCategory, url=category)
        return super().get(request, category=None, **kwargs)


class ProductView(View):
    """Контроллер для отображения выбранного товара"""
    model = Product

    def queryset(self, pk):
        return get_object_or_404(self.model, pk=pk)

    def get_context_data(self, pk):
        product = self.queryset(pk)
        context = {
            'title': product.name,
            'data': product
        }
        return context

    def get(self, request, pk):
        return render(request, 'mainapp/product.html', self.get_context_data(pk))


class ContactsView(View):
    """Контроллер для отображения контактной информации магазина"""

    title = 'Контакты'
    template_name = 'mainapp/contact.html'
    file = 'contacts.json'

    def get_contact_list(self):
        with open(os.path.join(FIXTURES_DIR, self.file), 'r') as read_file:
            return json.load(read_file)

    def get_context_data(self):
        context = {
            'title': self.title,
            'contacts': self.get_contact_list(),
        }
        return context

    def get(self, request):
        return render(request, self.template_name, self.get_context_data())
