from django.conf import settings
from django.urls import path

import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.ProductListView.as_view(), name='all_products'),
    path('<str:category>', mainapp.CategoryProductListView.as_view(), name='category'),
    path('category/<str:category>/page/<int:page>/', mainapp.CategoryProductListView.as_view(), name='category_page'),
    path('page/<int:page>/', mainapp.ProductListView.as_view(), name='page'),
]
