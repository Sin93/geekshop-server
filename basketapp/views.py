# Django
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.base import View
# Project
from basketapp.models import Basket
from mainapp.models import Product


class BasketView(View):
    """Контроллер для отображения корзины пользователя"""
    title = 'корзина'
    template_name = 'basketapp/basket.html'
    model = Basket

    def get_context_data(self):
        context = {
            'title': self.title,
            'basket_items': self.queryset(),
        }
        return context

    def queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get(self, request):
        return render(request, self.template_name, self.get_context_data())


class BasketAddView(View):
    """Контроллер для добавления товаров в корзину пользователя"""
    model = Basket

    @method_decorator(login_required())
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        basket = self.model.objects.filter(user=request.user, product=product).first()

        if not basket:
            basket = Basket(user=request.user, product=product)

        basket.quantity += 1
        basket.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class BasketRemoveView(View):
    """Контроллер для удаления товаров из корзины пользователя"""
    @method_decorator(login_required())
    def get(self, request, pk):
        basket_record = get_object_or_404(Basket, pk=pk)
        basket_record.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class BasketEditView(View):
    """Контроллер для изменения количества товаров в корзине пользователя.
    Получает запросы от JS, код размещён в static/js/basket.js"""
    def get_result(self, pk, quantity):
        result = {
            'result': quantity,
            'id': pk,
            'total_quantity': self.request.user.user_basket_quantity,
            'total_cost': self.request.user.user_basket_cost
        }
        return result

    @method_decorator(login_required())
    def get(self, request, pk, quantity):
        if request.is_ajax():
            basket_item = Basket.objects.get(pk=pk)

            if quantity > 0:
                basket_item.quantity = quantity
                basket_item.save()
                return JsonResponse(self.get_result(pk, quantity))
            elif quantity == 0:
                basket_item.delete()
                return JsonResponse(self.get_result(pk, 'delete'))
            else:
                return JsonResponse({'result': False})
