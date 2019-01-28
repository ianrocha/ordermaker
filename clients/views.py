from django.views.generic import ListView

from carts.models import Cart
from .models import Client


class ClientListView(ListView):
    template_name = 'clients/list.html'

    def get_context_data(self, *args, **kwargs):
        """
        Obtain all the clients in the database and the cart of session
        """
        context = super(ClientListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        return Client.objects.all()
