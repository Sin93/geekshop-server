import json

from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView
from django.views.generic.base import View

from basketapp.models import Basket
from ordersapp.models import Order, OrderItem


class OrdersView(ListView):
    """Контроллер для отображения заказов пользователя"""
    model = Order
    template_name = 'ordersapp/orders_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'заказы'

        return context

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user).exclude(status=Order.CANCEL)
        result = []

        for num, itm in enumerate(queryset):
            order_items = OrderItem.objects.filter(order=itm)
            result.append({
                'number': num+1,
                'order': itm,
                'order_items': order_items
            })

        return result


class OrderCreate(View):
    """Контроллер для создания заказа, работает в связке с static/js/basket.js
    Принимает ajax и возвращает json"""
    def get_baskets(self):
        return Basket.objects.filter(user=self.request.user)

    def post(self, request):
        if request.is_ajax():
            ajax_order = json.loads(request.body.decode('utf-8'))['order']  # содержимое ajax запроса
            json_response = {'result': True, 'order': [], 'errors': []}  # Заготовка для ответа
            result_actions = {'order': None, 'actions': []}  # Действия, которые будут выполнены если всё прошло успешно

            with transaction.atomic():
                order = Order(user=self.request.user)
                result_actions['order'] = order.save

                for key, value in ajax_order.items():
                    key, value = int(key), int(value)
                    basket = Basket.objects.get(pk=key)
                    product = basket.product
                    # Проверяем достаточно ли товара на складе, чтобы оформить заказ
                    if product.quantity < value:
                        json_response['result'] = False
                        json_response['errors'].append(f'{product.name} на складе: {product.quantity}')
                        continue

                    order_itm = OrderItem(order=order, product=product, quantity=value)
                    product.quantity = product.quantity - value
                    # если товара достаточно на складе, то добавить в список запланированных действий сохранение
                    result_actions['actions'].append(order_itm.save)
                    result_actions['actions'].append(product.save)
                    result_actions['actions'].append(basket.delete)

                    json_response['order'].append(key)

                if json_response['result']:
                    # Если все товары были в наличии выполнить каждое действие из списка result_actions['actions']
                    result_actions['order']()
                    for action in result_actions['actions']:
                        action()

                return JsonResponse({'result': json_response})


class OrderDelete(DeleteView):
    """Контроллер для отмены заказа самим пользователем"""
    model = Order
    success_url = reverse_lazy('ordersapp:orders_view')

