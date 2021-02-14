# Django
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.urls import reverse
# Project
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductAdminForm
from mainapp.models import Product, ProductCategory


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = 'admin - новый пользователь'

    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin_staff:users'))
    else:
        user_form = ShopUserRegisterForm()

    content = {'title': title, 'update_form': user_form}

    return render(request, 'adminapp/user_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    title = 'admin - пользователи'

    users_list = ShopUser.objects.all().order_by(
        '-is_active',
        '-is_superuser',
        '-is_staff',
        'username'
    )

    content = {
        'title': title,
        'objects': users_list
    }

    return render(request, 'adminapp/users.html', content)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    title = 'пользователи/редактирование'

    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        edit_form = ShopUserAdminEditForm(request.POST, request.FILES,\
                                                        instance=edit_user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_staff:users'))
    else:
        edit_form = ShopUserAdminEditForm(instance=edit_user)

    content = {'title': title, 'update_form': edit_form}

    return render(request, 'adminapp/user_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def user_change_active(request, pk):

    target_user = get_object_or_404(ShopUser, pk=pk)
    target_user.is_active = False if target_user.is_active else True
    target_user.save()

    return HttpResponseRedirect(reverse('admin_staff:users'))


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    if request.method == 'POST':
        edit_form = ProductCategoryEditForm(data=request.POST)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_staff:categories'))
        else:
            return HttpResponseRedirect(reverse('admin_staff:categories'))


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'admin - категории'

    categories_list = ProductCategory.objects.all()
    categories_and_forms = []
    for category in categories_list:
        categories_and_forms.append({'category': category, 'form': ProductCategoryEditForm(instance=category)})

    content = {
        'title': title,
        'objects': categories_and_forms,
        'new_category': ProductCategoryEditForm
    }

    return render(request, 'adminapp/categories.html', content)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    category = ProductCategory.objects.get(pk=pk)
    if request.method == 'POST':
        edit_form = ProductCategoryEditForm(data=request.POST, instance=category)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_staff:categories'))
        else:
            return HttpResponseRedirect(reverse('admin_staff:categories'))


@user_passes_test(lambda u: u.is_superuser)
def category_change_active(request, pk):
    target_category = get_object_or_404(ProductCategory, pk=pk)

    if target_category.is_active:
        target_category.is_active = False
        target_category.save()
        products_in_this_category = Product.objects.filter(category=target_category)

        if products_in_this_category:
            for product in products_in_this_category:
                product.is_active = False
                product.save()

    else:
        target_category.is_active = True
        target_category.save()

    return HttpResponseRedirect(reverse('admin_staff:categories'))


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
