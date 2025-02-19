from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from orders.forms import OrderForm
from orders.models import Order
from products.models import Basket

# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Store - Thank you for order!'


class CanceledView(TitleMixin, TemplateView):
    template_name = 'orders/canceled.html'
    title = 'Store - Cancel order'


class OrderListView(TitleMixin, ListView):
    template_name = 'orders/orders.html'
    title = 'Store - Orders'
    queryset = Order.objects.all()
    ordering = '-created'

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderView(TemplateView):
    template_name = 'orders/order.html'

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        context['object'] = Order.objects.get(pk=kwargs.get('order_id'))
        context['title'] = 'Store - Order'
        return context


class OrderCreateView(TitleMixin, CreateView):
    template_name = "orders/order-create.html"
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    title = "Store - Order Create"

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)

        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.stripe_products(),
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled')),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except:
        return HttpResponse(status=400)

    if (
        event['type'] == 'checkout.session.completed'
        or event['type'] == 'checkout.session.async_payment_succeeded'
    ):
        fulfill_checkout(event['data']['object'])

    return HttpResponse(status=200)


def fulfill_checkout(session):
    order = Order.objects.get(pk=int(session.metadata.order_id))
    order.update_after_payment()
