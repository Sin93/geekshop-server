from django.urls import path
from django.contrib import admin
import mainapp.views as mainapp

urlpatterns = [
    path('', mainapp.main, name='main'),
    path('products/', mainapp.products, name='products'),
    path('product/<int:id>', mainapp.view_product, name='product'),
    path('contact/', mainapp.contact, name='contact'),
    path('admin/', admin.site.urls),
]
