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

    objects = CartManager()

    def __str__(self):
        return str(self.id)


class CartItemQuerySet(models.query.QuerySet):
    def by_cart(self, cart):
        return self.filter(cart__exact=cart)


class CartItemManager(models.Manager):
    def get_queryset(self):
        return CartItemQuerySet(self.model, using=self._db)

    def by_cart(self, cart):
        return self.get_queryset().by_cart(cart)


class CartItem(models.Model):
    OPTIMUM = 'Optimum'
    GOOD = 'Good'
    BAD = 'Bad'

    PROFITABILITY_CHOICES = (
        (OPTIMUM, 'Optimum'),
        (GOOD, 'Good'),
        (BAD, 'Bad'),
    )

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(default=0.01, max_digits=100, decimal_places=2)
    default_quantity = models.PositiveIntegerField(default=1)
    default_price = models.DecimalField(default=0.01, max_digits=100, decimal_places=2)
    profitability = models.CharField(max_length=7, choices=PROFITABILITY_CHOICES, default=GOOD)

    objects = CartItemManager()

    def __str__(self):
        return str(self.id)
