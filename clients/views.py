from django.views.generic import ListView

from .models import Client


class ClientListView(ListView):
    template_name = 'clients/list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ClientListView, self).get_context_data(*args, **kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        return Client.objects.all()
