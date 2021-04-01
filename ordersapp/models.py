from django.db import models
from django.conf import settings

from mainapp.models import Product


class Order(models.Model):
    ORDER_IS_MADE = 'OM'
    PROCEEDED = 'PRD'
    READY = 'RDY'
    ISSUED = 'ISS'
    CANCEL = 'CNC'

    ORDER_STATUS_CHOICES = (
        (ORDER_IS_MADE, 'оформлен'),
        (PROCEEDED, 'собирается'),
        (READY, 'готов к выдаче'),
        (ISSUED, 'выдан'),
        (CANCEL, 'отменен'),
    )

    # удалять заказы пользователя если пользователь был удалён - не самая лучшая идея, по этому выставлю SET_NULL
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now=True)
    status = models.CharField(verbose_name='статус', max_length=3, choices=ORDER_STATUS_CHOICES, default=PROCEEDED)
    is_active = models.BooleanField(verbose_name='активен', default=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return 'Текущий заказ: {}'.format(self.id)

    def all_order_items(self):
        return OrderItem.objects.filter(order=self)

    def get_total_quantity(self):
        items = self.order_items.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_product_type_quantity(self):
        items = self.order_items.select_related()
        return len(items)

    def get_total_cost(self):
        items = self.order_items.select_related()
        return sum(list(map(lambda x: x.quantity * x.product.price, items)))

    def delete(self, **kwargs):
        for item in self.order_items.select_related():
            item.product.quantity += item.quantity
            item.product.save()

        self.is_active = False
        self.status = self.CANCEL
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='продукт', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=1)

    def get_product_cost(self):
        return self.product.price * self.quantity
