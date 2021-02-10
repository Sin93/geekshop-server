from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from basketapp.models import Basket
from mainapp.models import Product
from django.template.loader import render_to_string
from django.http import JsonResponse

@login_required
def basket(request):
    basket_items = Basket.objects.filter(user=request.user)

    content = {
        'title': 'корзина',
        'basket_items': basket_items,
        'basket_sum': basket_items[0].total_cost() if basket_items else None,
        'basket_quantity': basket_items[0].total_quantity() if basket_items else None,
    }

    return render(request, 'basketapp/basket.html', content)

@login_required
def basket_add(request, pk):
    product = get_object_or_404(Product, pk=pk)

    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    basket_item = Basket.objects.get(pk=int(pk))
    print(basket_item.quantity)
    if request.is_ajax():
        quantity = int(quantity)
        basket_item = Basket.objects.get(pk=int(pk))

        if quantity > 0:
            basket_item.quantity = quantity
            basket_item.save()
            print(basket_item.quantity)
        else:
            basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user).order_by('product__category')

        content = {
            'basket_items': basket_items,
        }

        result = render_to_string('basketapp/includes/inc_basket_list.html', content)

        return JsonResponse({'result': result})
