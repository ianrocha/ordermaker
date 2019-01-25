from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .forms import CartItemForm
from .models import Cart, CartItem
from clients.models import Client
from orders.models import Order
from products.models import Product
from ordermaker.utils import validate_quantity, validate_profitability


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    cart_items_obj = CartItem.objects.all().filter(cart=cart_obj)
    context = {'cart_items': cart_items_obj,
               'cart': cart_obj}
    return render(request, "carts/home.html", context)


def cart_update(request):
    product_id = request.POST.get('product_id')
    client_id = request.POST.get('client_id')
    cart_obj, new_obj = Cart.objects.new_or_get(request)

    if client_id is not None:
        try:
            client_obj = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            return redirect("cart:home")

        if client_obj == cart_obj.client:
            cart_obj.client = None
            cart_obj.save()
        else:
            cart_obj.client = client_obj
            cart_obj.save()

    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect("cart:home")

        cart_item_qs, item_created = CartItem.objects.get_or_create(cart=cart_obj, product=product_obj)
        if not item_created:
            cart_item_qs.delete()
            added = False
        else:
            cart_item_qs.cart = cart_obj
            cart_item_qs.product = product_obj
            cart_item_qs.quantity = product_obj.is_multiple
            cart_item_qs.default_quantity = product_obj.is_multiple
            cart_item_qs.price = product_obj.unit_price
            cart_item_qs.default_price = product_obj.unit_price
            cart_item_qs.profitability = 'Good'
            cart_item_qs.save()
            added = True

        cart_item_count = CartItem.objects.all().filter(cart=cart_obj)
        request.session['cart_items'] = cart_item_count.count()

        if request.is_ajax():
            json_data = {
                "added": added,
                "removed": not added,
                "cartItemCount": cart_item_count.count(),
            }
            return JsonResponse(json_data)

    return redirect('cart:home')


def cart_item_detail_api_view(request):
    cart = request.GET.get('cart')
    cart_item_obj = CartItem.objects.all().filter(cart=cart)
    cart_items = [{"id": x.id,
                   "cart": x.cart,
                   "product": x.product,
                   "quantity": x.quantity,
                   "price": x.price,
                   "profitability": x.profitability} for x in cart_item_obj]
    cart_data = {'cart_items': cart_items}
    return JsonResponse(cart_data)


class CartItemUpdateView(UpdateView):
    form_class = CartItemForm
    model = CartItem
    template_name = 'carts/cart-item-update-form.html'
    success_url = reverse_lazy('cart:home')

    def post(self, request, *args, **kwargs):
        quantity = int(request.POST.get('quantity'))
        default_quantity = int(request.POST.get('default_quantity'))
        result_ok = validate_quantity(quantity=quantity, default_quantity=default_quantity)

        if not result_ok:
            messages.error(request, "This item can only be sold in multiples of {}".format(default_quantity))
            return redirect('cart:item-update', pk=self.kwargs.get('pk'))

        profitability = request.POST.get('profitability')
        profitability_ok = validate_profitability(profitability)

        if not profitability_ok:
            messages.error(request, "Items can't have a bad profitability!")
            return redirect('cart:item-update', pk=self.kwargs.get('pk'))

        return super(CartItemUpdateView, self).post(request, *args, **kwargs)


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    cart_items = CartItem.objects.all().filter(cart=cart_obj)

    if cart_created or cart_items.count() == 0:
        return redirect('cart:home')

    order_obj, order_obj_created = Order.objects.new_or_get(cart_obj)

    if request.method == 'POST':
        client = order_obj.cart.client
        if client is not None:
            order_obj.mark_paid()
            request.session['cart_items'] = 0
            del request.session['cart_id']
            return redirect('cart:success')
        else:
            messages.error(request, 'Cart has no client! Please choose one.')
            return redirect('cart:home')

    context = {
        'object': order_obj,
        'cart_items': cart_items,
    }

    return render(request, 'carts/checkout.html', context)


def checkout_done_view(request):
    return render(request, 'carts/checkout-done.html', {})
