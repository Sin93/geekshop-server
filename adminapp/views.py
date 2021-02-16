# Django
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
# Project
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductAdminForm
from mainapp.models import Product, ProductCategory


class CheckStaffMixine:
    """Добавлена проверка на принадлежность к персоналу, для метода dispatch.
    dispatch - метод базового класса View для всех CBV."""

    @method_decorator(user_passes_test(lambda u: u.is_superuser or u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)


class UcersListView(CheckStaffMixine, ListView):
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


class UserCreateView(CheckStaffMixine, CreateView):
    model = ShopUser
    form_class = ShopUserAdminEditForm
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin_staff:users')


class UserUpdateView(CheckStaffMixine, UpdateView):
    model = ShopUser
    form_class = ShopUserAdminEditForm
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin_staff:users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи/редактирование'

        return context


class UserChangeActiveView(CheckStaffMixine, DeleteView):
    model = ShopUser
    success_url = reverse_lazy('admin_staff:users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False if self.object.is_active else True
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class CategoriesView(CheckStaffMixine, ListView):
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


class CategoryCreateView(CheckStaffMixine, CreateView):
    model = ProductCategory
    form_class = ProductCategoryEditForm
    success_url = reverse_lazy('admin_staff:categories')


class CategoryUpdateView(CheckStaffMixine, UpdateView):
    model = ProductCategory
    form_class = ProductCategoryEditForm
    success_url = reverse_lazy('admin_staff:categories')


class CategoryChangeActiveView(CheckStaffMixine, DeleteView):
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


@user_passes_test(lambda u: u.is_superuser)
def products(request, category=None):

    content = {
        'title': 'admin - товары',
    }

    objects = []

    if category:
        target_category = get_object_or_404(ProductCategory, url=category)
        content['category'] = target_category
        products = Product.objects.filter(category=target_category).order_by('name')

        content['objects'] = objects
    else:
        products = Product.objects.all().order_by('-is_active', 'category__name')

    for product in products:
        objects.append({
            'product':product,
            'form': ProductAdminForm(instance=product)
        })

    content['objects'] = objects
    content['new_product'] = ProductAdminForm()

    return render(request, 'adminapp/products.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request):
    if request.method == 'POST':
        edit_form = ProductAdminForm(data=request.POST, files=request.FILES)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_staff:categories'))
        else:
            return HttpResponseRedirect(reverse('admin_staff:categories'))


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        edit_form = ProductAdminForm(data=request.POST, files=request.FILES, instance=product)
        if edit_form.is_valid():
            edit_form.save()
            print(request.META.get('HTTP_REFERER'))
            if request.META.get('HTTP_REFERER').split('/')[-2] != 'category':
                return HttpResponseRedirect(reverse(
                    'admin_staff:products',
                    args=([request.META.get('HTTP_REFERER').split('/')[-2]])
                    ))
            else:
                return HttpResponseRedirect(reverse('admin_staff:all_products'))
        else:
            return HttpResponseRedirect(reverse('admin_staff:all_products'))


@user_passes_test(lambda u: u.is_superuser)
def product_change_active(request, pk):
    target_product = get_object_or_404(Product, pk=pk)
    if target_product.category.is_active:
        if target_product.is_active:
            target_product.is_active = False
        else:
            target_product.is_active = True

        target_product.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        warning = f'Категория товара "{target_product.name}": "{target_product.category.name}" - деактивирована, нельзя активировать товар в неактивной категории. Для активации товара измените его категорию.'

        content = {
            'title': 'admin - товары',
            'warning': warning
        }

        objects = []

        if request.META.get('HTTP_REFERER').split('/')[-2] != 'category':
            category = request.META.get('HTTP_REFERER').split('/')[-2]
            target_category = get_object_or_404(ProductCategory, url=category)
            content['category'] = target_category
            products = Product.objects.filter(category=target_category).order_by('name')
        else:
            products = Product.objects.all().order_by('-is_active', 'category__name')

        for product in products:
            objects.append({
                'product':product,
                'form': ProductAdminForm(instance=product)
            })

        content['objects'] = objects

        return render(request, 'adminapp/products.html', content)
