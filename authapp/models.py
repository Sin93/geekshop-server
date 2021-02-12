from django.db import models
from django.contrib.auth.models import AbstractUser
from basketapp.models import Basket


class ShopUser(AbstractUser):
    avatar = models.ImageField(verbose_name='аватар', upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name = 'возраст', blank=True, null=True)

    @property
    def user_basket_cost(self):
        return sum([basket_itm.quantity * basket_itm.product.price for basket_itm in Basket.objects.filter(user_id=self.id)])

    @property
    def user_basket_quantity(self):
        return sum([basket_itm.quantity for basket_itm in Basket.objects.filter(user_id=self.id)])
