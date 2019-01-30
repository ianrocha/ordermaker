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
    """
    List all products on cart, initialize checkout
    """
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    cart_items_obj = CartItem.objects.by_cart(cart=cart_obj)
    context = {'cart_items': cart_items_obj,
               'cart': cart_obj}
    return render(request, "carts/home.html", context)


def cart_update(request):
    """
    Remove or add an item/client to a cart
    """
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
        # Verifies if item is already on cart
        if not item_created:
            # If it is then, remove item from cart
            cart_item_qs.delete()
            added = False
        else:
            cart_item_qs.save()
            added = True

        # Refresh number of items on cart
        cart_item_count = CartItem.objects.by_cart(cart=cart_obj)
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
    """
    Refresh cart items
    """
    cart = request.GET.get('cart')
    cart_item_obj = CartItem.objects.by_cart(cart=cart)
    cart_items = [{"id": x.id,
                   "cart": x.cart,
                   "product": x.product,
                   "quantity": x.quantity,
                   "price": x.price,
                   "profitability": x.profitability} for x in cart_item_obj]
    cart_data = {'cart_items': cart_items}
    return JsonResponse(cart_data)


class CartItemUpdateView(UpdateView):
    """
    Update View for Cart Item records
    """
    form_class = CartItemForm
    model = CartItem
    template_name = 'carts/cart-item-update-form.html'
    success_url = reverse_lazy('cart:home')

    def post(self, request, *args, **kwargs):
        quantity = int(request.POST.get('quantity'))
        default_quantity = int(request.POST.get('default_quantity'))

        # Validate if the 'quantity' inputted by user is acceptable
        result_ok = validate_quantity(quantity=quantity, default_quantity=default_quantity)

        if not result_ok:
            messages.warning(request, "This item can only be sold in multiples of {}".format(default_quantity))
            return redirect('cart:item-update', pk=self.kwargs.get('pk'))

        profitability = request.POST.get('profitability')
        # Validate if the 'profitability' inputted by user is acceptable
        profitability_ok = validate_profitability(profitability)

        if not profitability_ok:
            messages.warning(request, "Items can't have a bad profitability!")
            return redirect('cart:item-update', pk=self.kwargs.get('pk'))

        return super(CartItemUpdateView, self).post(request, *args, **kwargs)


def checkout_home(request):
    """
    Finalize checkout, closing cart and marking order has paid
    """
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    cart_items = CartItem.objects.by_cart(cart=cart_obj)

    if cart_created or cart_items.count() == 0:
        return redirect('cart:home')

    order_obj, order_obj_created = Order.objects.new_or_get(cart_obj)

    if request.method == 'POST':
        # Get the client
        client = order_obj.cart.client
        if client is not None:
            # If cart has a client, do the checkout
            # Change Order status to paid
            order_obj.mark_paid()
            # set session cart items to 0
            request.session['cart_items'] = 0
            # delete cart from session
            del request.session['cart_id']
            return redirect('cart:success')
        else:
            messages.warning(request, 'Cart has no client! Please choose one.')
            return redirect('cart:home')

    context = {
        'object': order_obj,
        'cart_items': cart_items,
    }

    return render(request, 'carts/checkout.html', context)


def checkout_done_view(request):
    return render(request, 'carts/checkout-done.html', {})
