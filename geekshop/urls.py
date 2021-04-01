from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import include
from django.urls import path, re_path
from django.views.generic import RedirectView

import mainapp.views as mainapp


urlpatterns = [
    path('', mainapp.MainView.as_view(), name='main'),
    path('', include('social_django.urls', namespace='social')),
    path('index/<str:message>', mainapp.MainView.as_view(), name='main_with_msg'),
    path('product/<int:pk>', mainapp.ProductView.as_view(), name='product'),
    path('products/', include('mainapp.urls', namespace='mainapp')),
    path('contact/', mainapp.ContactsView.as_view(), name='contact'),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('admin/', admin.site.urls),
    path('admin-staff/', include('adminapp.urls', namespace='admin_staff')),
    path('basket/', include('basketapp.urls', namespace='basket')),
    path('order/', include('ordersapp.urls', namespace='order')),
    re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico'), name='favicon'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
