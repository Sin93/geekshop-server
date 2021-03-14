from django.db import models
from django.contrib.auth.models import AbstractUser
from basketapp.models import Basket
from django.utils.timezone import now
from datetime import timedelta


class ShopUser(AbstractUser):
    avatar = models.ImageField(verbose_name='аватар', upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст', blank=True, null=True)
    activation_key = models.CharField(verbose_name='ключ активации', max_length=128, blank=True, null=True)
    activation_key_expires = models.DateTimeField(default=(now() + timedelta(hours=48)))

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True

    @property
    def user_basket_cost(self):
        return sum([basket_itm.quantity * basket_itm.product.price for basket_itm in Basket.objects.filter(user_id=self.id)])

    @property
    def user_basket_quantity(self):
        return sum([basket_itm.quantity for basket_itm in Basket.objects.filter(user_id=self.id)])
