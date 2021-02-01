from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

import mainapp.views as mainapp


urlpatterns = [
    path('', mainapp.main, name='main'),
    path('all_products/', mainapp.products, name='all_products'),
    path('products/<str:category>', mainapp.products, name='products'),
    path('product/<int:id>', mainapp.view_product, name='product'),
    path('contact/', mainapp.contact, name='contact'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
