from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView

from carts.forms import CartItemForm
from .models import Order
from carts.models import CartItem
from ordermaker.utils import validate_quantity, validate_profitability


class OrderListView(ListView):
    template_name = 'orders/list.html'

    def get_queryset(self):
        return Order.objects.get_paid_only()


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

    def get_context_data(self, **kwargs):
        context = super(OrderItemUpdateView, self).get_context_data()
        context['order_id'] = self.kwargs.get('order_id')
        return context

    def get_success_url(self):
        return reverse('orders:detail', kwargs={'order_id': self.kwargs.get('order_id')})

    def post(self, request, *args, **kwargs):
        quantity = int(request.POST.get('quantity'))
        default_quantity = int(request.POST.get('default_quantity'))
        result_ok = validate_quantity(quantity=quantity, default_quantity=default_quantity)

        if not result_ok:
            messages.error(request, "This item can only be sold in multiples of {}".format(default_quantity))
            return redirect('orders:order-item-update', order_id=self.kwargs.get('order_id'), pk=self.kwargs.get('pk'))

        profitability = request.POST.get('profitability')
        profitability_ok = validate_profitability(profitability)

        if not profitability_ok:
            messages.error(request, "Items can't have a bad profitability!")
            return redirect('orders:order-item-update', order_id=self.kwargs.get('order_id'), pk=self.kwargs.get('pk'))

        return super(OrderItemUpdateView, self).post(request, *args, **kwargs)
