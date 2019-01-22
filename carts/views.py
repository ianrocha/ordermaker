from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .forms import CartItemForm
from .models import Cart, CartItem
from clients.models import Client
from products.models import Product


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
                   "price": x.price} for x in cart_item_obj]
    cart_data = {'cart_items': cart_items}
    return JsonResponse(cart_data)


class CartItemUpdateView(UpdateView):
    form_class = CartItemForm
    model = CartItem
    template_name = 'carts/cart_item_update_form.html'
    success_url = reverse_lazy('cart:home')
