import adminapp.views as adminapp
from django.urls import path

app_name = 'adminapp'

urlpatterns = [
    path('users/create/', adminapp.UserCreateView.as_view(), name='user_create'),
    path('users/read/', adminapp.UsersListView.as_view(), name='users'),
    path('users/update/<int:pk>/', adminapp.UserUpdateView.as_view(), name='user_update'),
    path('users/change_active/<int:pk>/', adminapp.UserChangeActiveView.as_view(), name='user_change_active'),

    path('categories/create/', adminapp.CategoryCreateView.as_view(), name='category_create'),
    path('categories/read/', adminapp.CategoriesView.as_view(), name='categories'),
    path('categories/update/<int:pk>/', adminapp.CategoryUpdateView.as_view(), name='category_update'),
    path(
        'categories/change_active/<int:pk>/',
        adminapp.CategoryChangeActiveView.as_view(),
        name='category_change_active'
    ),

    path('products/create/', adminapp.ProductCreateView.as_view(), name='product_create'),
    path('products/create/<str:category>/', adminapp.ProductCreateView.as_view(), name='product_create_in_category'),
    path('products/read/category/', adminapp.ProductListView.as_view(), name='all_products'),
    path('products/read/category/<str:category>/', adminapp.ProductListView.as_view(), name='products'),
    path('products/update/<int:pk>/', adminapp.ProductUpdateView.as_view(), name='product_update'),
    path('products/change_active/<int:pk>/', adminapp.ProductChangeActiveView.as_view(), name='product_change_active'),
]
