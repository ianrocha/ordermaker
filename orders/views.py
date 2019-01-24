from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView

from carts.forms import CartItemForm
from .models import Order
from carts.models import CartItem


class OrderListView(ListView):
    template_name = 'orders/list.html'

    def get_queryset(self):
        return Order.objects.all()


class OrderDetailView(DetailView):
    template_name = 'orders/detail.html'

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data()
        cart_obj = self.object.cart
        cart_items_obj = CartItem.objects.all().filter(cart__exact=cart_obj)
        context['cart_items'] = cart_items_obj
        return context

    def get_object(self, queryset=None):
        qs = Order.objects.all().filter(order_id=self.kwargs.get('order_id'))
        if qs.count() == 1:
            return qs.first()
        raise Http404


class OrderItemUpdateView(UpdateView):
    form_class = CartItemForm
    model = CartItem
    template_name = 'orders/order-item-update.html'

    def get_success_url(self):
        return reverse('orders:detail', kwargs={'order_id': self.kwargs.get('order_id')})
