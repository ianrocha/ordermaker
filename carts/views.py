from django.http import JsonResponse
from django.shortcuts import render, redirect

from .models import Cart, CartItem
from products.models import Product


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    cart_itens_obj = CartItem.objects.all().filter(cart=cart_obj)
    context = {'cart_itens': cart_itens_obj,
               'cart': cart_obj}
    return render(request, "carts/home.html", context)


def cart_update(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect("cart:home")

        cart_obj, new_obj = Cart.objects.new_or_get(request)
        cart_item_qs, item_created = CartItem.objects.get_or_create(cart=cart_obj, product=product_obj)
        if not item_created:
            cart_item_qs.delete()
            added = False
        else:
            cart_item_qs.cart = cart_obj
            cart_item_qs.product = product_obj
            cart_item_qs.quantity = product_obj.is_multiple
            cart_item_qs.price = product_obj.unit_price
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
            print(json_data)
            return JsonResponse(json_data)

    return redirect('cart:home')
