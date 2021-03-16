from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import include
from django.urls import path, re_path
from django.views.generic import RedirectView

import mainapp.views as mainapp


urlpatterns = [
    path('', mainapp.main, name='main'),
    path('index/<str:message>', mainapp.main, name='main_with_msg'),
    path('product/<int:id>', mainapp.view_product, name='product'),
    path('products/', include('mainapp.urls', namespace='mainapp')),
    path('contact/', mainapp.contact, name='contact'),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('social/', include('social_django.urls', namespace='social')),
    path('admin/', admin.site.urls),
    path('admin-staff/', include('adminapp.urls', namespace='admin_staff')),
    path('basket/', include('basketapp.urls', namespace='basket')),
    re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico'), name='favicon'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
