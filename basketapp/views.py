from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from basketapp.models import Basket
from mainapp.models import Product


def basket(request):
    basket_items = Basket.objects.filter(user=request.user)

    content = {
        'title': 'корзина',
        'basket_items': basket_items,
    }

    content['basket_sum'] = Basket.basket_sum(request.user)

    return render(request, 'basketapp/basket.html', content)


def basket_add(request, pk):
    product = get_object_or_404(Product, pk=pk)

    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
