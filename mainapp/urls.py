from django.conf import settings
from django.urls import path

import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
        path('', mainapp.products, name='all_products'),
        path('<str:category>', mainapp.products, name='category'),
    ]
