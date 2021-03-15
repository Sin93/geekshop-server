# Django
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
# Project
from authapp.models import ShopUser
from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductAdminForm
from mainapp.models import Product, ProductCategory


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
        return super().dispatch(request, *args, **kwargs)


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


class UserChangeActiveView(GeekShopMixin, DeleteView):
    """Контроллер для активации/деактивации пользователя в админке"""
    model = ShopUser
    success_url = reverse_lazy('admin_staff:users')

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False if user.is_active else True
        user.save()

        return HttpResponseRedirect(self.get_success_url())


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
        category = self.get_object()
        category.is_active = False if category.is_active else True
        category.save()

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
    model = Product
    form_class = ProductAdminForm
    success_url = reverse_lazy('admin_staff:all_products')

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


class ProductUpdateView(GeekShopMixin, UpdateView):
    model = Product
    form_class = ProductAdminForm
    success_url = reverse_lazy('admin_staff:all_products')

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


@user_passes_test(lambda u: u.is_superuser)
def product_change_active(request, pk):
    """Контроллер для активации/деактивации товара.
    с помощью CBV пока не смог добиться необходимого уровня кастомизации"""
    target_product = get_object_or_404(Product, pk=pk)
    if target_product.category.is_active:
        if target_product.is_active:
            target_product.is_active = False
        else:
            target_product.is_active = True

        target_product.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        warning = f'Категория товара "{target_product.name}": "{target_product.category.name}" - деактивирована, ' \
                  f'нельзя активировать товар в неактивной категории. Для активации товара измените его категорию.'

        content = {
            'title': 'admin - товары',
            'warning': warning
        }

        if request.META.get('HTTP_REFERER').split('/')[-2] != 'category':
            category = request.META.get('HTTP_REFERER').split('/')[-2]
            target_category = get_object_or_404(ProductCategory, url=category)
            content['category'] = target_category
            products = Product.objects.filter(category=target_category).order_by('name')
        else:
            products = Product.objects.all().order_by('-is_active', 'category__name')

        for product in products:
            setattr(product, 'form', ProductAdminForm(instance=product))

        content['object_list'] = products

        return render(request, 'adminapp/products.html', content)


# class ProductChangeActiveView(GeekShopMixin, DeleteView):
#     model = Product
#     success_url = reverse_lazy('admin_staff:all_products')
#     template_name = None
#     warning = None
#
#     def delete(self, request, *args, **kwargs):
#         product = self.get_object()
#         if product.category.is_active:
#             product.is_active = False if product.is_active else True
#             product.save()
#         else:
#             self.warning = f'Категория товара "{product.name}": "{product.category.name}" - деактивирована, ' +\
#                 'нельзя активировать товар в неактивной категории. Для активации товара измените его категорию.'
#
#         return HttpResponseRedirect(self.get_success_url())
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.warning:
#             context['warning'] = self.warning
#
#         return context
#
#     def get_success_url(self):
#         return self.request.META.get('HTTP_REFERER')
