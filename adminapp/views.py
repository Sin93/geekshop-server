# Django
import json

from django.contrib.auth.decorators import user_passes_test
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView
# Project
from authapp.models import ShopUser
from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductAdminForm, OrderItemForm
from mainapp.models import Product, ProductCategory
from ordersapp.models import Order, OrderItem


class GeekShopMixin(View):
    """Проверка на принадлежность к персоналу, для метода dispatch.
    dispatch - метод базового класса View для всех CBV."""

    def get_category(self):
        try:
            return get_object_or_404(ProductCategory, url=self.kwargs['category'])
        except KeyError:
            return None

    def get_product(self):
        try:
            return get_object_or_404(Product, pk=self.kwargs['pk'])
        except KeyError:
            return None

    @method_decorator(user_passes_test(lambda u: u.is_superuser or u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)


class UsersListView(GeekShopMixin, ListView):
    """Контроллер для отображения списка пользователей в админке"""
    model = ShopUser
    template_name = 'adminapp/users.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'admin - пользователи'

        return context

    def get_queryset(self):
        return ShopUser.objects.all().order_by(
            '-is_active',
            '-is_superuser',
            '-is_staff',
            'username'
        )


class UserCreateView(GeekShopMixin, CreateView):
    """Контроллер для создания пользователя"""
    model = ShopUser
    form_class = ShopUserAdminEditForm
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin_staff:users')


class UserUpdateView(GeekShopMixin, UpdateView):
    """Контроллер для изменения пользователя в админке"""
    model = ShopUser
    form_class = ShopUserAdminEditForm
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin_staff:users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи/редактирование'

        return context


class UserChangeActiveView(GeekShopMixin):
    """Контроллер для активации/деактивации пользователя в админке"""
    model = ShopUser
    pk = None
    success_url = reverse_lazy('admin_staff:users')

    def get_object(self):
        return get_object_or_404(self.model, pk=self.pk)

    def post(self, request, pk):
        self.pk = pk
        user = self.get_object()
        user.is_active = False if user.is_active else True
        user.save()

        return HttpResponseRedirect(self.success_url)


class CategoriesView(GeekShopMixin, ListView):
    """Контроллер для отображения категорий товаров в админке"""
    model = ProductCategory
    template_name = 'adminapp/categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'admin - категории'
        object_list = context['object_list']

        categories_and_forms = []
        for category in object_list:
            categories_and_forms.append({'category': category, 'form': ProductCategoryEditForm(instance=category)})

        context['object_list'] = categories_and_forms
        context['new_category'] = ProductCategoryEditForm

        return context

    def get_queryset(self):
        return ProductCategory.objects.all().order_by('-is_active', 'name')


class CategoryCreateView(GeekShopMixin, CreateView):
    """Контроллер для создания новой категории товаров в админке"""
    model = ProductCategory
    form_class = ProductCategoryEditForm
    success_url = reverse_lazy('admin_staff:categories')


class CategoryUpdateView(GeekShopMixin, UpdateView):
    """Контроллер для изменения категории товаров в админке"""
    model = ProductCategory
    form_class = ProductCategoryEditForm
    success_url = reverse_lazy('admin_staff:categories')


class CategoryChangeActiveView(GeekShopMixin, DeleteView):
    """Контроллер для активации/деактивации категорий товаров в админке"""
    model = ProductCategory
    success_url = reverse_lazy('admin_staff:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False if self.object.is_active else True
        self.object.save()

        if not self.object.is_active:
            products_in_this_category = Product.objects.filter(category=self.object)
            for product in products_in_this_category:
                product.is_active = False
                product.save()

        return HttpResponseRedirect(self.get_success_url())


class ProductListView(GeekShopMixin, ListView):
    """Контроллер для отображения товаров (опционально - отображение товаров по категориям)"""
    model = ProductCategory
    template_name = 'adminapp/products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_category()

        if category:
            context['category'] = category
            context['title'] = f'admin - товары({category.name})'
        else:
            context['title'] = 'admin - все товары'

        context['new_product'] = ProductAdminForm()
        return context

    def get_queryset(self):
        category = self.get_category()

        if category:
            queryset = Product.objects.filter(category=category).order_by('-is_active', 'name')
        else:
            queryset = Product.objects.all().order_by('-is_active', 'category__name')

        for product in queryset:
            # добавляем форму к объектам товаров, нужно для редактирования
            setattr(product, 'form', ProductAdminForm(instance=product))

        return queryset


class ProductCreateView(GeekShopMixin, CreateView):
    """Контроллер для создания товара"""
    model = Product
    form_class = ProductAdminForm
    success_url = reverse_lazy('admin_staff:all_products')

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


class ProductUpdateView(GeekShopMixin, UpdateView):
    """Контроллер для изменения товара"""
    model = Product
    form_class = ProductAdminForm
    success_url = reverse_lazy('admin_staff:all_products')

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


class ProductChangeActive(GeekShopMixin):
    """Контроллер для активации/деактивации товара"""

    @staticmethod
    def get_context_data(request, warning=None):
        context = {}

        # Если указана категория, то будем выводить товары категории, в противном случае выведем всё
        if request.META.get('HTTP_REFERER').split('/')[-2] != 'category':
            category = request.META.get('HTTP_REFERER').split('/')[-2]
            target_category = get_object_or_404(ProductCategory, url=category)
            context['title'] = f'admin - товары({target_category.name})'
            context['category'] = target_category
            products = Product.objects.filter(category=target_category).order_by('name')
        else:
            products = Product.objects.all().order_by('-is_active', 'category__name')
            context['title'] = 'admin - все товары'

        # Каждому товару добавляем в атрибуты форму для изменения
        for product in products:
            setattr(product, 'form', ProductAdminForm(instance=product))

        context['object_list'] = products
        context['new_product'] = ProductAdminForm()  # форма для нового товара

        # если есть предупреждение, то выводим его
        if warning:
            context['warning'] = warning

        return context

    def post(self, request, pk):
        target_product = get_object_or_404(Product, pk=pk)

        # Проверяем активна ли категория в которой находится товар
        if target_product.category.is_active:
            target_product.is_active = False if target_product.is_active else True
            target_product.save()

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            # Если категория не активна, то надо вывести предупреждение
            warning = f'Категория товара "{target_product.name}": "{target_product.category.name}" - деактивирована, ' \
                      f'нельзя активировать товар в неактивной категории. Для активации товара измените его категорию.'
            context = self.get_context_data(request, warning)

            return render(request, 'adminapp/products.html', context)


class StaffOrderList(GeekShopMixin, ListView):
    """Контроллер для отображения всех заказов"""
    model = Order
    template_name = 'adminapp/order_list.html'
    title = 'Все заказы'
    ordering = ['updated', '-is_active']
    filter = None
    OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.filter(is_active=True, quantity__gte=1).order_by('category__name')
        context['products'] = products
        context['title'] = self.title
        return context

    def get_queryset(self):
        if self.filter:
            queryset = self.model.objects.filter(status=self.filter)
        else:
            queryset = self.model.objects.all()
        for order in self.ordering:
            queryset = queryset.order_by(order)

        return queryset


class StaffOrderProcessedList(StaffOrderList):
    """Контроллер для отображения ещё не собранных заказов"""
    filter = Order.PROCEEDED
    title = 'Заказы на сборку'


class StaffOrderReadyList(StaffOrderList):
    """Контроллер для отображения заказов готовых к выдаче"""
    filter = Order.READY
    title = 'Заказы на выдачу'


class StaffOrderIsReady(GeekShopMixin):
    """Контроллер для изменения статуса заказа на "готов к выдаче" """
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.status = Order.READY
        order.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class StaffOrderIssued(GeekShopMixin):
    """Контроллер для изменения статуса заказа на "выдан" """
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.status = Order.ISSUED
        order.is_active = False
        order.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class StaffOrderUpdate(GeekShopMixin, UpdateView):
    """Контроллер для изменения заказа на отдельной странице с применением formset"""
    model = Order
    template_name = 'adminapp/order.html'
    fields = []
    success_url = reverse_lazy('adminapp:all_orders')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        if self.request.POST:
            context['formset'] = OrderFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = OrderFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        order_items = context['formset']

        with transaction.atomic():
            print(form.data)
            form.instance.user = self.request.user
            self.object = form.save()
            if order_items.is_valid():
                order_items.instance = self.object
                order_items.save()

        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


class StaffAddOrderItem(GeekShopMixin):
    """Контроллер для добавления товара в заказ со страницы со всеми товарами.
    Ajax запрос посылает скрипт static/js/order_staff.js, он же и обрабатывает ответ"""
    def post(self, request):
        if request.is_ajax():
            ajax = json.loads(request.body.decode('utf-8'))
            order = Order.objects.get(pk=ajax.get('order'))
            order_items = order.all_order_items()
            product = Product.objects.get(pk=ajax.get('product'))
            for itm in order_items:
                if itm.product == product:
                    return JsonResponse({
                        'result': False,
                        'error': f'ОШИБКА! {product.name} ({product.category.name}) - есть в заказе!'
                    })
            if product.quantity > 0:
                product.quantity -= 1
                product.save()
                new_order_item = OrderItem(order=order, product=product, quantity=1)
                new_order_item.save()
                result = {
                    'result': True,
                    'name': product.name,
                    'price': product.price,
                    'order_item_pk': new_order_item.pk
                }
                return JsonResponse(result)


class StaffChangeOrder(GeekShopMixin):
    """Контроллер для изменения заказа со страницы со всеми товарами.
        Ajax запрос посылает скрипт static/js/order_staff.js, он же и обрабатывает ответ"""
    @staticmethod
    def plus(order_item, product):
        if product.quantity > 0:
            order_item.quantity += 1
            order_item.save()
            product.quantity -= 1
            product.save()
            return {
                'result': True,
                'order_item_quantity': order_item.quantity,
                'order_item_cost': order_item.get_product_cost(),
                'order': order_item.order.pk,
                'order_sum': order_item.order.get_total_cost()
            }
        else:
            return {
                'result': False,
                'error': f'Недостаточно товара на складе!'
            }

    @staticmethod
    def minus(order_item, product):
        if order_item.quantity > 1:
            order_item.quantity -= 1
            order_item.save()
            product.quantity += 1
            product.save()
            return {
                'result': True,
                'order_item_quantity': order_item.quantity,
                'order_item_cost': order_item.get_product_cost(),
                'order': order_item.order.pk,
                'order_sum': order_item.order.get_total_cost()
            }
        else:
            product.quantity += 1
            product.save()
            order = order_item.order
            order_item.delete()
            return {
                'result': True,
                'order_item_quantity': 0,
                'order_item_cost': 0,
                'order': order.pk,
                'order_sum': order.get_total_cost()
            }

    @staticmethod
    def delete(order_item, product):
        product.quantity += order_item.quantity
        product.save()
        order = order_item.order
        order_item.delete()
        return {
            'result': True,
            'order_item_quantity': 0,
            'order_item_cost': 0,
            'order': order.pk,
            'order_sum': order.get_total_cost()
        }

    def post(self, request):
        if request.is_ajax():
            ajax = json.loads(request.body.decode('utf-8'))
            order_item = OrderItem.objects.get(pk=ajax.get('order_item'))
            product = order_item.product

            if ajax.get('action') == 'plus':
                result = self.plus(order_item, product)
            elif ajax.get('action') == 'minus':
                result = self.minus(order_item, product)
            elif ajax.get('action') == 'delete':
                result = self.delete(order_item, product)
            else:
                result = {
                    'result': False,
                    'error': 'ОШИБКА!'
                }

            result['order_item_pk'] = order_item.pk

            return JsonResponse(result)


class StaffOrderDelete(GeekShopMixin, DeleteView):
    """Контроллер для отмены заказа из админки.
    На всякий случай, чтобы не забыть: в модели Order переопределён метод delete(), при "удалении" объекта,
    товар сам возвращается на склад, а заказ деактивируется."""
    model = Order
    success_url = reverse_lazy('admin_staff:all_orders')
