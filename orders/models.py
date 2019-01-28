import random
import string

from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse

from carts.models import Cart, CartItem


ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
)


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    """
    :return: A new random string
    """
    return ''.join(random.choice(chars) for _ in range(size))


def unique_order_id_generator():
    """
    :return: A new random order id
    """
    order_new_id = random_string_generator()
    return order_new_id


class OrderManager(models.Manager):
    def new_or_get(self, cart_obj):
        created = False
        qs = self.get_queryset().filter(cart=cart_obj, active=True, status='created')
        if qs.count() == 1:
            obj = qs.first()
        else:
            created = True
            obj = self.model.objects.create(cart=cart_obj)
        return obj, created

    def get_paid_only(self):
        """
        :return: A queryset filtered by orders with status 'paid' only
        """
        qs = self.get_queryset().filter(status__exact='paid')
        return qs


class Order(models.Model):
    order_id = models.CharField(max_length=120, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = OrderManager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.order_id

    def get_absolute_url(self):
        return reverse('orders:detail', kwargs={'order_id': self.order_id})

    def mark_paid(self):
        """
        Change order status to 'paid'
        """
        if self.status != 'paid':
            self.status = 'paid'
            self.save()
        return self.status


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    """
    Obtain the order id before saving it
    """
    if not instance.order_id:
        instance.order_id = unique_order_id_generator()


pre_save.connect(pre_save_create_order_id, sender=Order)
