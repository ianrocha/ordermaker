from django.db import models

from clients.models import Client
from products.models import Product


class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get('cart_id', None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            cart_obj.save()
        else:
            cart_obj = Cart.objects.new()
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self):
        return self.model.objects.create()


class Cart(models.Model):
    client = models.ForeignKey(Client, blank=True, null=True, on_delete=models.CASCADE)
    total = models.DecimalField(default=0.0, max_digits=100, decimal_places=2)

    objects = CartManager()

    def __str__(self):
        return str(self.id)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(default=0.0, max_digits=100, decimal_places=2)

    def __str__(self):
        return str(self.id)