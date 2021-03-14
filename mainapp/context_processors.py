from basketapp.models import Basket


def basket(request):
    user_basket = []
    if request.user.is_authenticated:
        user_basket = Basket.objects.filter(user=request.user)

    return {
       'basket': user_basket,
    }
