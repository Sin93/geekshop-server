from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import mainapp.views as mainapp


urlpatterns = [
    path('', mainapp.main, name='main'),
    path('product/<int:id>', mainapp.view_product, name='product'),
    path('products/', include('mainapp.urls', namespace='mainapp')),
    path('contact/', mainapp.contact, name='contact'),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
