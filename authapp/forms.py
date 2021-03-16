from authapp.models import ShopUser, ShopUserProfile
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
import hashlib
import random


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(ShopUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'password1', 'password2', 'email', 'age', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if len(first_name) < 5:
            raise forms.ValidationError("слишком короткое имя пользователя!")

        return first_name

    def save(self, *args, **kwargs):
        user = super(ShopUserRegisterForm, self).save()

        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()

        return user


class ShopUserEditForm(UserChangeForm):
    avatar = forms.ImageField(widget=forms.FileInput, required=False)

    class Meta:
        model = ShopUser
        fields = ('username', 'email', 'first_name', 'age', 'avatar', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()
            if field_name == 'avatar':
                field.label = 'Аватар'

        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True

    def clean_username(self):
        form_username = self.cleaned_data['username']
        if form_username != self.instance.username and not self.instance.is_superuser:
            raise forms.ValidationError("нельзя меня UserName!")

        return form_username

    def clean_email(self):
        form_email = self.cleaned_data['email']
        if form_email != self.instance.email and not self.instance.is_superuser:
            raise forms.ValidationError("нельзя меня Email!")

        return form_email

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if len(first_name) < 5:
            raise forms.ValidationError("слишком короткое имя пользователя!")

        return first_name


class ShopUserProfileEditForm(forms.ModelForm):
    class Meta:
        model = ShopUserProfile
        fields = ('tagline', 'aboutMe', 'gender')

    def __init__(self, *args, **kwargs):
        super(ShopUserProfileEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
