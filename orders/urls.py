from django.urls import path

from orders.views import (CanceledView, OrderCreateView, OrderListView,
                          OrderView, SuccessView)

app_name = 'orders'
urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('order-success/', SuccessView.as_view(), name='order_success'),
    path('order-canceled/', CanceledView.as_view(), name='order_canceled'),
    path('', OrderListView.as_view(), name='orders_list'),
    path('<int:order_id>/', OrderView.as_view(), name='order'),
]
