# Django
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import Http404
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
# Project
from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, ShopUserProfileEditForm
from authapp.models import ShopUser
from authapp.utils import send_verify_email


def verify(request, user_id, hash):
    user = ShopUser.objects.get(pk=user_id)

    if user.activation_key == hash and not user.is_activation_key_expired():
        user.is_active = True
        user.activation_key = None
        user.save()
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect(reverse('main_with_msg', args=['successful_verify']))

    return Http404()


def login(request):
    login_form = ShopUserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main'))

    content = {
        'title': 'вход',
        'login_form': login_form
    }

    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)

    return HttpResponseRedirect(reverse('main'))


def register(request):
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(data=request.POST, files=request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            send_verify_email(user)
            return HttpResponseRedirect(reverse('main_with_msg', args=['successful_register']))
    else:
        register_form = ShopUserRegisterForm()

    content = {
        'title': 'регистрация',
        'register_form': register_form
    }

    return render(request, 'authapp/register.html', content)


@login_required
@transaction.atomic
def edit(request):
    if request.method == 'POST':
        edit_form = ShopUserEditForm(data=request.POST, files=request.FILES, instance=request.user)
        edit_profile_form = ShopUserProfileEditForm(data=request.POST, instance=request.user.profile)
        if edit_form.is_valid() and edit_profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('main'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        edit_profile_form = ShopUserProfileEditForm(instance=request.user.profile)

    content = {
        'title': 'редактирование',
        'edit_form': edit_form,
        'profile_form': edit_profile_form,
    }

    return render(request, 'authapp/edit.html', content)
