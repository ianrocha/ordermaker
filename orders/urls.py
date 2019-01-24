from django.urls import path

from .views import OrderListView, OrderDetailView, OrderItemUpdateView


urlpatterns = [
    path('', OrderListView.as_view(), name='list'),
    path('<order_id>/', OrderDetailView.as_view(), name='detail'),
    path('<order_id>/edit/item/<pk>', OrderItemUpdateView.as_view(), name='order-item-update')
]
