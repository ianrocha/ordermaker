import random
import string

from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.text import slugify

from carts.models import Cart, CartItem


ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
)


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    klass = instance.__class__
    qs_exists = klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(slug=slug, randstr=random_string_generator(size=4))
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def unique_order_id_generator(instance, new_slug=None):
    order_new_id = random_string_generator()

    klass = instance.__class__
    qs_exists = klass.objects.filter(order_id=order_new_id).exists()
    if qs_exists:
        return unique_slug_generator(instance)
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
        qs = self.get_queryset().filter(status__exact='paid')
        return qs


class Order(models.Model):
    order_id = models.CharField(max_length=120, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    active = models.BooleanField(default=True)

    objects = OrderManager()

    def __str__(self):
        return self.order_id

    def get_absolute_url(self):
        return reverse('orders:detail', kwargs={'order_id': self.order_id})

    def mark_paid(self):
        if self.status != 'paid':
            self.status = 'paid'
            self.save()
        return self.status


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)


pre_save.connect(pre_save_create_order_id, sender=Order)
