from django.urls import path

from ordersapp.views import *

app_name = 'ordersapp'

urlpatterns = [
    path('', OrdersView.as_view(), name='orders_view'),
    path('create_order/', OrderCreate.as_view(), name='create_order'),
    path('delete_order/<int:pk>', OrderDelete.as_view(), name='delete_order'),
]
