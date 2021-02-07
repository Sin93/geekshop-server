from django.db import models
from django.conf import settings
from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add=True)

    @staticmethod
    def basket_sum(user):
        total_cost = 0
        total_quantity = 0
        basket = Basket.objects.filter(user=user)
        for itm in basket:
            total_cost += itm.quantity * itm.product.price
            total_quantity += itm.quantity

        return {'total_cost': total_cost, 'total_quantity': total_quantity}
