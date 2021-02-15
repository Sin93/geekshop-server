import adminapp.views as adminapp
from django.urls import path

app_name = 'adminapp'

urlpatterns = [
    path('users/create/', adminapp.user_create, name='user_create'),
    path('users/read/', adminapp.users, name='users'),
    path('users/update/<int:pk>/', adminapp.user_update, name='user_update'),
    path('users/change_active/<int:pk>/', adminapp.user_change_active, name='user_change_active'),

    path('categories/create/', adminapp.category_create, name='category_create'),
    path('categories/read/', adminapp.categories, name='categories'),
    path('categories/update/<int:pk>/', adminapp.category_update, name='category_update'),
    path('categories/change_active/<int:pk>/', adminapp.category_change_active, name='category_change_active'),

    path('products/create/category/', adminapp.product_create, name='product_create'),
    path('products/read/category/', adminapp.products, name='all_products'),
    path('products/read/category/<str:category>/', adminapp.products, name='products'),
    path('products/update/<int:pk>/', adminapp.product_update, name='product_update'),
    path('products/change_active/<int:pk>/', adminapp.product_change_active, name='product_change_active'),
]
