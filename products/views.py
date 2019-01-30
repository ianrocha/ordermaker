from django.views.generic import ListView

from carts.models import Cart, CartItem
from .models import Product


class ProductListView(ListView):
    template_name = 'products/list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        :return: Context with the cart and a list of items that are already in cart
        """
        context = super(ProductListView, self).get_context_data()
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        cart_items = CartItem.objects.by_cart(cart=cart_obj)
        cart_items_obj = [item.product for item in cart_items]
        context['cart'] = cart_obj
        context['cart_items'] = cart_items_obj
        return context

    def get_queryset(self, *args, **kwargs):
        """
        :return: All products of database
        """
        return Product.objects.all()
