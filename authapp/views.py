# Django
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.http import Http404
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.base import View
# Project
from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, ShopUserProfileEditForm
from authapp.models import ShopUser
from authapp.utils import send_verify_email


class VerifyView(View):
    redirect_to = 'main_with_msg'
    redirect_with_args = ['successful_verify']

    def get(self, request, user_id, hash):
        user = ShopUser.objects.get(pk=user_id)

        if user.activation_key == hash and not user.is_activation_key_expired():
            user.is_active = True
            user.activation_key = None
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect(reverse(self.redirect_to, args=self.redirect_with_args))

        return Http404()


class LoginView(View):
    title = 'вход'
    template_name = 'authapp/login.html'
    login_form = ShopUserLoginForm

    def get_context_data(self):
        context = {
            'title': self.title,
            'login_form': self.login_form()
        }
        return context

    def post(self, request):
        if request.method == 'POST' and self.login_form(data=request.POST).is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main'))

    def get(self, request):
        return render(request, self.template_name, self.get_context_data())


class LogoutView(View):
    redirect_to = 'main'

    def get(self, request):
        auth.logout(request)
        return HttpResponseRedirect(reverse(self.redirect_to))


class RegisterView(View):
    title = 'регистрация'
    template_name = 'authapp/register.html'
    form = ShopUserRegisterForm
    redirect_to = 'main_with_msg'
    redirect_with_args = ['successful_register']

    def get_context_data(self):
        context = {
            'title': self.title,
            'register_form': self.form
        }
        return context

    def post(self, request):
        register_form = self.form(data=request.POST, files=request.FILES)
        if register_form.is_valid():
            user = register_form.save()
            send_verify_email(user)
            return HttpResponseRedirect(reverse('main_with_msg', args=['successful_register']))

    def get(self, request):
        return render(request, self.template_name, self.get_context_data())


class UserEditView(View):
    title = 'редактирование'
    template_name = 'authapp/edit.html'
    redirect_to = 'main'
    account_form = ShopUserEditForm
    profile_form = ShopUserProfileEditForm

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self):
        context = {
            'title': self.title,
            'edit_form': self.account_form(instance=self.request.user),
            'profile_form': self.profile_form(instance=self.request.user.profile)
        }
        return context

    @transaction.atomic
    def post(self, request):
        edit_account_form = self.account_form(data=request.POST, files=request.FILES, instance=request.user)
        edit_profile_form = self.profile_form(data=request.POST, instance=request.user.profile)
        if edit_account_form.is_valid() and edit_profile_form.is_valid():
            edit_account_form.save()
            return HttpResponseRedirect(reverse(self.redirect_to))

    def get(self, request):
        return render(request, self.template_name, self.get_context_data())
